
import unittest
from copy import deepcopy
from . import checks

class TestChecks(unittest.TestCase):
    def test_ownership_check(self):
        testFeature = {
                "type":"Feature",
                "geometry":{
                    "type":"Point",
                    "coordinates":[1,1]
                    },
                "properties":{
                    "author_id":1
                    }
            }
        self.assertTrue(checks.check_geojson_ownership(testFeature,1))
        self.assertFalse(checks.check_geojson_ownership(testFeature,2))

        testFc = {
                "type":"FeatureCollection",
                "features":[testFeature]
            }

        self.assertTrue(checks.check_geojson_ownership(testFc,1))

        other = deepcopy(testFeature)
        other["properties"]["author_id"] = 2
        other["properties"]["foo"] = "bar"
        testFc["features"].append(other)

        self.assertFalse(checks.check_geojson_ownership(testFc,1))
