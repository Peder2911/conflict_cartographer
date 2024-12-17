
import re
import os
import json
import urllib

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from api.views import whoami
from api.models import Country

class ApiViewsTest(TestCase):
    def test_whoami(self):
        r = self.client.get(reverse("whoami"),follow=True)
        url,code = r.redirect_chain[-1]
        self.assertEqual(code,302)
        self.assertIsNotNone(url,re.search("next=/api/whoami",url))
        self.assertIsNotNone(url,re.search("accounts/login",url))

        u = User.objects.create_user(
                username="nemo",
                password="nemo"
                )
        self.client.login(username="nemo",password="nemo")
        r = self.client.get(reverse("whoami"))
        self.assertEqual(r.status_code,200)

        self.assertEqual(r.json(),{
                "name": "nemo",
                "waiver": False
            })

    def test_country_detail(self):
        u = User.objects.create_user(username="adder",password="adder")
        c = Country.objects.create(
                name="Somewhere",
                shape={"shape":"here"},
                simpleshape={"also":"a shape"},
                iso2c="sw",
                gwno=123)

        u.profile.countries.set([c])
        self.client.login(username="adder",password="adder")

        path = reverse("country-detail",args=(c.gwno,))+"?format=json"
        r = self.client.get(path)
        self.assertEqual(r.status_code,404)
        c.active = True
        c.save()

        r = self.client.get(path)
        self.assertEqual(r.status_code,200)
        self.assertDictEqual(r.json(),{
            "shape":{"shape":"here"},
            "url":"http://testserver"+path,
            "name":"Somewhere",
            "iso2c":"sw",
            "gwno":123,
        })

    def test_nocountries(self):
        u = User.objects.create_user(username="meep",password="meep")
        self.client.login(username="meep",password="meep")
        r = self.client.get(reverse("assigned"))
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json()["countries"],[])
    
    def test_baddata(self):
        u = User.objects.create_user(username="bad",password="bad")
        c = Country.objects.create(name="x",iso2c="xx",gwno=10,shape={},simpleshape={},active=True)
        u.profile.countries.set([c])
        u.profile.save()

        self.client.login(username="bad",password="bad")

        assigned = self.client.get(reverse("assigned")).json()
        ctry = assigned["countries"][0]

        r = self.client.post(reverse("shape-list"),data="Hello world!",content_type="text")
        self.assertEqual(r.status_code,415)

        r = self.client.post(reverse("shape-list"),data={
                "something":"wrong",
            },content_type="application/json")
        self.assertEqual(r.status_code,400)

        r = self.client.post(reverse("shape-list"),data={
                "values":{
                    "a":"B"
                },
                "country":ctry["url"]
            },content_type="application/json")
        self.assertEqual(r.status_code,400)

        r = self.client.post(reverse("shape-list"),data={
                "shape":{
                    "a":"B"
                    },
                "country":ctry["url"]
            },content_type="application/json")
        self.assertEqual(r.status_code,400)

        r = self.client.post(reverse("shape-list"),data={
                "shape":{"type":"Point","coordinates":[1,1]},
                "values":{
                    "a":1,
                    "b":2
                },
                "country":ctry["url"]
            },content_type="application/json")
        self.assertEqual(r.status_code,201)

    def test_util_views(self):
        u = User.objects.create_user(username="someone",password="something")
        self.client.login(username="someone",password="something")
        r = self.client.get(reverse("hasprofiledata"))
        self.assertEqual(r.status_code,200)
        self.assertFalse(r.json()["profile"])

        u.profile.meta = {"something":"weird"}
        u.profile.save()

        r = self.client.get(reverse("hasprofiledata"))
        self.assertEqual(r.status_code,200)
        self.assertTrue(r.json()["profile"])
