import json

from datetime import date,timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from api.models import Country,Shape,NonAnswer
from api.testutils import ApiTestCase,randomFeature

class QuarterizingTest(ApiTestCase):
    def setUp(self):
        self.u = User.objects.create_user(username="test",password="test")
        self.u2 = User.objects.create_user(username="test2",password="test2")

        self.c = Country.objects.create(name="nowhere",iso2c="NW",shape={},simpleshape={},gwno=1)
        self.client.login(username="test",password="test")
        self.u.profile.countries.set([self.c])

    def test_quarterizing(self):
        Shape.objects.create(
                author=self.u,date=date.today()-timedelta(weeks=32),
                shape={},country=self.c,values={})

        r = self.client.get(reverse("shape-list"))
        self.assertEqual(len(json.loads(r.content.decode())),0)

        s = Shape.objects.create(author=self.u, shape={},country=self.c,values={})
        self.assertEqual(s.date,date.today())

        s,data = self.shapes_get()
        self.assertEqual(len(data),1)

    def test_mutex_answers(self):
        r = self.client.get(reverse("assigned"))
        assigned_countries = json.loads(r.content.decode())
        first_country = assigned_countries["countries"][0]
        #c,*_ = json.loads(r.content.decode())

        s = Shape.objects.create(
                date = date.today()-timedelta(weeks=52),
                author = self.u,
                country = self.c,
                shape = {},
                values = {}
            )

        na = NonAnswer.objects.create(
                date = date.today()-timedelta(weeks=104),
                author = self.u,
                country = self.c
                )

        su2 = Shape.objects.create(
                author = self.u2,
                country = self.c,
                shape = {},
                values = {}
            )

        static = ((NonAnswer,na),(Shape,s),(Shape,su2))
        # Ensure that all of the above still exist.
        for m,o in static:
            try:
                m.objects.get(pk=o.pk)
            except m.DoesNotExist:
                self.fail()

        self.shapes_post(shape=randomFeature(),country=first_country["url"],values={"a":"b"})

        s,data = self.project_status(first_country["gwno"])
        self.assertEqual(data["shapes"],1)
        self.assertFalse(data["nonanswer"])

        
        self.nonanswer(first_country["gwno"])

        s,data = self.project_status(first_country["gwno"])
        self.assertEqual(data["shapes"],0)
        self.assertTrue(data["nonanswer"])


        self.shapes_post(shape={},country=first_country["url"],values={"c":"d"})

        s,data = self.project_status(first_country["gwno"])
        self.assertEqual(data["shapes"],1)
        self.assertFalse(data["nonanswer"])

        # Ensure that static are untouched. 
        for m,o in static:
            try:
                m.objects.get(pk=o.pk)
            except m.DoesNotExist:
                self.fail()
