import json

import geojson

from django.test import TestCase
from django.urls import reverse

def randomFeature():
    return {
        "type":"Feature",
        "geometry": geojson.utils.generate_random("Polygon"),
        "properties":{}
    }

def returnData(inner):
    def wrapper(*args,**kwargs):
        r = inner(*args,**kwargs)
        try:
            data = json.loads(r.content)
        except:
            data = None
        return r.status_code,data
    return wrapper

def returnContent(inner):
    def wrapper(*args,**kwargs):
        r = inner(*args,**kwargs)
        return r.status_code,r.content
    return wrapper

class ApiTestCase(TestCase):
    """
    Terse testing of the API through call-methods.
    """

    @returnContent
    def shapes_post(self,**kwargs):
        return self.client.post(reverse("shape-list"),kwargs,content_type="application/json")

    @returnContent
    def shapes_put(self,pk,**kwargs):
        return self.client.put(reverse("shape-detail",args=(pk,)),kwargs,content_type="application/json")

    @returnContent
    def shapes_delete(self,pk):
        return self.client.delete(reverse("shape-detail",args=(pk,)))

    @returnData
    def project_status(self,pk):
        return self.client.get(reverse("projectstatus",kwargs={"project":pk}))

    @returnData
    def project_assigned(self):
        return self.client.get(reverse("assigned"))

    @returnContent
    def nonanswer(self,project):
        return self.client.post(reverse("nonanswer",kwargs={"project":project}))

    @returnData
    def shapes_get(self,project=None):
        url = reverse("shape-list")
        if project:
            url += f"?country={project}"
        return self.client.get(url)

    @returnData
    def shapes_detail(self,pk):
        return self.client.get(reverse("shape-detail",args=(pk,)))
