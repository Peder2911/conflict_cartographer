import json
from datetime import date,datetime
from unittest.mock import patch,Mock

import geojson

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from django.utils.timezone import now

from api.testutils import randomFeature
from api.views import projectStatus,clearShapes
from api.models import Country,Shape,NonAnswer
from api.views import ShapeViewSet

class TestStatusViews(TestCase):
    def setUp(self):
        self.u = User.objects.create_superuser(username = "test", password="test")
        self.u.save()
        
    def test_project_status(self):
        c = Country(gwno=1,name="Somewhere",iso2c="SW",shape={},simpleshape={})
        c.save()

        with patch("cartographer.services.today",Mock(return_value=date(1999,6,1))):
            url = reverse(projectStatus,kwargs={"project":1})
            r = self.client.get(url)
            self.assertEqual(r.status_code,403) # Redirects if not logged in

            login = self.client.login(username="test",password="test")
            r = self.client.get(url)
            self.assertEqual(r.status_code,200) 
            data = json.loads(r.content.decode())
            self.assertEqual(data["shapes"],0)

            na = NonAnswer(author = self.u, country = c, date=date(1999,6,1))
            na.save()

            data  = json.loads(self.client.get(url).content.decode())
            self.assertTrue(data["nonanswer"])

            s = Shape.objects.create(
                    author=self.u,
                    country=c,
                    date=date(1998,6,1),
                    shape = randomFeature()
                )
            data  = json.loads(self.client.get(url).content.decode())
            self.assertTrue(data["nonanswer"])
            self.assertEqual(data["shapes"],0)

            s = Shape.objects.create(
                    author=self.u,
                    country=c,
                    date=date(1999,1,1),
                    shape=randomFeature()
                )

            data  = json.loads(self.client.get(url).content.decode())
            self.assertTrue(data["nonanswer"])
            self.assertEqual(data["shapes"],0)

            s = Shape.objects.create(
                    author=self.u,
                    country=c,
                    date=date(1999,10,1),
                    shape=randomFeature()
                )

            data  = json.loads(self.client.get(url).content.decode())
            self.assertTrue(data["nonanswer"])
            self.assertEqual(data["shapes"],0)

            s = Shape.objects.create(
                    author=self.u,
                    country=c,
                    date=date(1999,6,15),
                    shape=randomFeature())
            
            data  = json.loads(self.client.get(url).content.decode())

            self.assertFalse(data["nonanswer"])
            self.assertEqual(data["shapes"],1)
