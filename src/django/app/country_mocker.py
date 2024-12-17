
from api.models import Country
from . import mock_data_creator

class CountryMocker(mock_data_creator.MockDataCreator):
    class Meta:
        model = Country
def load_countries():
    def _load_countries(self):
        with open(pkg_resources.resource_filename(__name__, "data/simpler_world.geojson")) as f:
            data = json.load(f)
        return data

    def _create_country(self, feature):
        return Country(
                gwno = feature["properties"]["gwno"],
                name = feature["properties"]["name"],
                iso2c = feature["properties"]["iso2c"],
                shape = feature["geometry"],
                simpleshape = feature["geometry"],
            )

    def _mock(self):
        for feature in self._load_countries()["features"]:
            country = self._create_country(feature)
            country.save()
