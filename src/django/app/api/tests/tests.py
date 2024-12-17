
import json
import unittest

from pydantic import ValidationError
from django.test import TestCase as DjangoTestCase
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from api.validation import CountryFeature,CountryFeatureCollection,CountryProps 
from api.views import updateCountries
from api.models import Country,ProjectDescription

class ValidationTest(unittest.TestCase):
    def test_geojson_val(self):
        try:
            cf = CountryFeature(
                    type="Feature",
                    geometry={
                        "type":"Polygon",
                        "coordinates": [[.1,.1],[.2,.2],[.3,.3],[.1,.1]]
                    },
                    properties = {
                        "CNTRY_NAME":"nowhere",
                        "GWCODE":9090,
                        "ISO1AL2":"BF"
                    }
                )

            cfc = CountryFeatureCollection(
                    type="FeatureCollection",
                    features=[cf]
                )
        except:
            self.fail()

        def fails():
            CountryFeature(
                    geometry={
                        "type":"Polygon",
                        "coordinates":[[.1,.1],[.2,.2],[.3,.3],[.1,.1]]
                        },
                    properties={
                        "foo":"bar"
                    }
                )
        self.assertRaises(ValidationError,fails)

        def fails():
            CountryFeature(
                    geometry={
                        "type":"Point",
                        "coordinates":[.1,.1]
                        },
                    properties={
                        "CNTRY_NAME":"somewhere",
                        "GWCODE":9090,
                        "ISO1AL2":"FG"
                    }
                )
        self.assertRaises(ValidationError,fails)

class TestCtryDataUpload(DjangoTestCase):
    def test_upload(self):
        mockCoord = [
                    [.1,.1],
                    [.2,.2],
                    [.3,.3],
                    [.1,.1]
                ]

        mockFeatures = [
                {
                    "type":"Feature",
                    "geometry":{
                        "type":"Polygon",
                        "coordinates":mockCoord
                    },
                    "properties":{
                        "CNTRY_NAME":"somewhere",
                        "GWCODE":999,
                        "ISO1AL2":"SM"
                    }
                },
                {
                    "type":"Feature",
                    "geometry":{
                        "type":"MultiPolygon",
                        "coordinates":[mockCoord,mockCoord]
                    },
                    "properties":{
                        "CNTRY_NAME":"nowhere",
                        "GWCODE":888,
                        "ISO1AL2":"NW"
                    }
                }
            ]


        cdata = {
            "small": {
                    "type":"FeatureCollection",
                    "features": mockFeatures
                },
            "large": {
                    "type":"FeatureCollection",
                    "features": mockFeatures
                }
        }

        su = User.objects.create_superuser(username="admin",password="admin")
        url = reverse("updatecountries")
        r = self.client.post(url,{})
        self.assertEqual(r.status_code,403)

        self.client.login(username="admin",password="admin")
        r = self.client.post(reverse("updatecountries"),{},content_type="application/json")
        self.assertEqual(r.status_code,400)

        r = self.client.post(reverse("updatecountries"),cdata,content_type="application/json")
        rd = json.loads(r.content.decode())
        self.assertEqual(rd["saved"],2)
        self.assertEqual(rd["updated"],0)
        self.assertEqual(r.status_code,200)
        self.assertEqual(len(Country.objects.all()),2)

        r = self.client.post(reverse("updatecountries"),cdata,content_type="application/json")
        rd = json.loads(r.content.decode())
        self.assertEqual(rd["saved"],0)
        self.assertEqual(rd["updated"],2)
        self.assertEqual(r.status_code,200)
        self.assertEqual(len(Country.objects.all()),2)

class OnlyOneActiveTest(DjangoTestCase):
    def test_ooa(self):

        pda = ProjectDescription(title="",description="",long_description="",active=True)
        pda.save()

        pdb = ProjectDescription(title="",description="",long_description="",active=True)
        pdb.save()

        self.assertEqual(len(ProjectDescription.objects.all().filter(active=True)),1)

