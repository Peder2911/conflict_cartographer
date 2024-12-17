
import logging
import faker
from . import user_mocker, country_mocker, prediction_mocker, meta_mocker, meta_mocker

logger = logging.getLogger(__name__)

class DatabaseMocker():
    def __init__(self, n_users: int, max_predictions_per_user_country: int, user_password: str):
        self._faker             = faker.Faker()
        self._country_mocker    = country_mocker.CountryMocker()
        self._user_mocker       = user_mocker.UserMocker(n_users, user_password, self._faker)
        self._prediction_mocker = prediction_mocker.PredictionMocker(max_predictions_per_user_country)
        self._meta_mocker = meta_mocker.MetaMocker(faker_instance = self._faker)

    def mock(self):
        logger.info("Mocking metadata")
        self._meta_mocker.mock()
        logger.info("Mocking countries")
        self._country_mocker.mock()
        logger.info("Mocking users and profiles")
        self._user_mocker.mock()
        logger.info("Mocking predictions")
        self._prediction_mocker.mock()
