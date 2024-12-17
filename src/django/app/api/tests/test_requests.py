"""
Testing API requests
"""
import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from api.models import Country
from api.testutils import ApiTestCase

class ApiRequestsTest(ApiTestCase):
    serialized_rollback = True

    def setUp(self):
        self.u = User.objects.create_user(username="testuser",password="12345")
        c = Country.objects.create(name="somewhere",iso2c="SW",gwno=1,shape={},simpleshape={})
        self.u.profile.countries.set([c])

    def test_crud(self):
        # Test disallowed without login
        for method,url in [("get","assigned"),("post","shape-list")]:
            self.assertEqual(getattr(self.client,method)(reverse(url)).status_code,403)

        login = self.client.login(username="testuser",password="12345")
        self.assertTrue(login)

        # Get assigned countries
        s, assigned = self.project_assigned()
        countries = assigned["countries"]
        self.assertEqual(s,200)
        self.assertEqual(countries[0]["gwno"],1)

        # Test posting a shape
        requestData = {
            "shape":{},
            "values":{
                "intensity":5,
                "confidence":5,
            },
            "country":countries[0]["url"]
            }

        s,c = self.shapes_post(**requestData)
        self.assertEqual(s,201)
        self.assertEqual(set(json.loads(c).keys()),
                {"url","country","shape","values","date"}
            )

        # Test posting a shape with arbitrary data
        requestData = {
            "shape":{},
            "values":{"something":"else","entirely":[1,2,3,4,5]},
            "country":countries[0]["url"]
            }

        s,c = self.shapes_post(**requestData)
        self.assertEqual(s,201)

        # Assert that data is properly stored 
        s,shapes = self.shapes_get(project=countries[0]["gwno"])
        self.assertEqual(s,200)

        s1,s2 = shapes

        self.assertEqual(s1["values"],{"intensity":5,"confidence":5})
        self.assertEqual(s2["values"],{"something":"else","entirely":[1,2,3,4,5]})

        # Assert that project status is correct 
        s,data = self.project_status(1)
        self.assertEqual(s,200)
        self.assertEqual(data["shapes"],2)

        # Delete a shape 

        self.client.delete(s1["url"])
        s,data = self.project_status(1)
        self.assertEqual(s,200)
        self.assertEqual(data["shapes"],1)

        # Update a shape 
        s2["values"] = {"a third option":3}
        r = self.client.put(s2["url"],data=s2,content_type="application/json")
        self.assertEqual(r.status_code,200)

        r = self.client.get(s2["url"])
        data = json.loads(r.content.decode())
        s = r.status_code
        self.assertEqual(s,200)
        self.assertEqual(data,s2)
