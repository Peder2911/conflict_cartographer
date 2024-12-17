import logging
import random
from typing import Tuple, List
from django.contrib.auth.models import User
from api.models import Shape, Country, Profile
from geomock import ops, random_geometry
from toolz import compose,curry
import shapely_geojson
from shapely import affinity, geometry
from . import mock_data_creator, randomness

logger = logging.getLogger(__name__)

def jitter(offset_noise, shape):
    return affinity.translate(shape, 
        xoff = random.random()*offset_noise,
        yoff = random.random()*offset_noise,
        zoff = random.random()*offset_noise)

class PredictionMocker(mock_data_creator.MockDataCreator):
    class Meta:
        model = Shape
        depends_on = {Country, Profile}

    def __init__(self, max_predictions_per_user_country: int):
        self._n = max_predictions_per_user_country

    @property
    def user_countries(self) -> Tuple[User, List[Country]]:
        for profile in Profile.objects.all():
            yield (profile.user, profile.countries)

    def _add_predictions(self, user, country):
        country_shape = geometry.shape(country.shape)
        
        move = compose(
                curry(jitter, .5),
                curry(ops.recenter, country_shape.centroid))

        n_preds = int(random.random() * self._n)

        logger.info(f"Adding {n_preds} predictions for {user.email}")

        shapes = []
        for _ in range(n_preds):
            geom = move(random_geometry.polygon(5,.9))

            props = {
                    "intensity": int(random.random()*2),
                    "confidence": int(random.random()*100)
                }

            shape = Shape(
                    author = user,
                    date = randomness.random_past_date(),
                    country = country,
                    shape = {"type": "Feature", "geometry": shapely_geojson.mapping(geom), "properties": props},
                    null_prediction = False,
                    values = props)
            shapes.append(shape)
        return shapes


    def _mock(self):
        for user,countries in self.user_countries:
            shapes = []

            for country in countries.all():
                shapes += self._add_predictions(user, country)

            for shape in shapes:
                shape.save()
