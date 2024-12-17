
import faker
from . import mock_data_creator
from api.models import ProjectDescription

class MetaMocker(mock_data_creator.MockDataCreator):
    class Meta:
        model = ProjectDescription

    def __init__(self, faker_instance: faker.Faker):
        self._faker = faker_instance

    def _mock(self):
        pj = ProjectDescription(
                title = "Conflict Cartographer",
                description = self._faker.text(),
                long_description = self._faker.text(max_nb_chars = 3000),
                active = True,
                )
        pj.save()




