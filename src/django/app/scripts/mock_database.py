
import logging
from django.conf import settings
from mocking import database_mocker

logging.basicConfig(level = logging.INFO)

def run():
    mocker = database_mocker.DatabaseMocker(
            n_users                          = settings.MOCK_N_USERS,
            max_predictions_per_user_country = settings.MOCK_MAX_PREDICTIONS_PER_USER_COUNTRY,
            user_password                    = settings.MOCK_USER_PASSWORD)

    mocker.mock()
