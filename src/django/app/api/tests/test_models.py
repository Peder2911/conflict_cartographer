
from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from api.models import Answer, Country

class TestApiModels(TestCase):
    def test_time_methods(self):
        u = User.objects.create_user(username="sphinx",password="1234")
        c = Country.objects.create(gwno = 1, name = "Somewhere", shape = {}, simpleshape = {}, iso2c = "SW")
        aw = Answer(
                date = date(year=1999,month=1,day=1),
                author = u,
                country = c
            )
        self.assertEqual(aw.quarter, 1)
        self.assertEqual(aw.year, 1999)
