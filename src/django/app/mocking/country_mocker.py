
import json
import pkg_resources
import logging
from . import mock_data_creator
from api.models import Country

logger = logging.getLogger(__name__)

class CountryMocker(mock_data_creator.MockDataCreator):
    class Meta:
        model = Country

    def _mock(self):
        with open(pkg_resources.resource_filename(__name__, "data/simpler_world.geojson")) as f:
            data = json.load(f)

        for country in data["features"]:
            c = Country(
                    gwno = country["properties"]["gwno"],
                    name = country["properties"]["name"],
                    iso2c = country["properties"]["iso2c"],
                    shape = country["geometry"],
                    simpleshape = country["geometry"],
                    active = True,
                )
            logger.info(f"Adding country: {c.name}") 

            c.save()

