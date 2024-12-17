
import random
import logging
from django.contrib.auth.models import User
from api.models import Country, Profile
import faker
from . import mock_data_creator, randomness

logger = logging.getLogger(__name__)

class UserMocker(mock_data_creator.MockDataCreator):
    class Meta:
        model = User

    def __init__(self, n: int, user_password: str, faker_instance: faker.Faker):
        self._faker = faker_instance 
        self._n = n
        self._user_password = user_password

    def _create_user(self, id: int) -> User:
        user_email = self._faker.email()

        user = User.objects.create_user(
                id = id,
                username = user_email,
                email = user_email,
                password = self._user_password,
            )

        logger.info(f"Created user: {user.email}")

        return user

    def _create_profile(self, user: User) -> Profile:
        assigned = set()

        for _ in range(5):
            assigned |= {Country.objects.order_by("?").first()}

        profile = Profile.objects.create(
                user = user,
                meta = {
                    "profession": self._faker.job(),
                    "affiliation": self._faker.company()
                    },
                waiver = bool(random.randint(0,1)),
                last_mailed = randomness.random_past_date(),
                unsubscribed = random.random() > .75
                )

        logger.info(f"Created profile: {profile.user.email}")

        profile.countries.set(list(assigned))

        return profile

    def _mock(self):
        for id in range(self._n):
            user = self._create_user(id)
            profile = self._create_profile(user)

            user.save()
            profile.save()
