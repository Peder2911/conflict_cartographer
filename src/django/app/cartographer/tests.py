import datetime
from django.test import TestCase
from cartographer.services import getQuarter,currentQuarter,quarters,quarterRange
from unittest.mock import patch

from datetime import date
import calendar

lastday = lambda y,m: calendar.monthrange(y,m)[1]

class ServiceTests(TestCase):

    def test_time_serv(self):
        self.assertEqual(getQuarter(datetime.date(1999,1,1)),1)
        self.assertEqual(getQuarter(datetime.date(1999,4,1)),2)
        self.assertEqual(getQuarter(datetime.date(1999,7,1)),3)
        self.assertEqual(getQuarter(datetime.date(1999,10,1)),4)

    def test_qrange(self):
        qr = quarterRange(datetime.date(year=1999,month=2,day=10))
        self.assertEqual(quarterRange(datetime.date(year=1999,month=2,day=10)),(
                datetime.date(year=1999,month=1,day=1),
                datetime.date(year=1999,month=3,day=lastday(1999,3))
            ))

        self.assertEqual(quarterRange(datetime.date(year=2001,month=4,day=10)),(
                datetime.date(year=2001,month=4,day=1),
                datetime.date(year=2001,month=6,day=lastday(2001,6))
            ))

        self.assertEqual(quarterRange(datetime.date(year=2001,month=8,day=10)),(
                datetime.date(year=2001,month=7,day=1),
                datetime.date(year=2001,month=9,day=lastday(2001,9))
            ))

        self.assertEqual(quarterRange(datetime.date(year=2001,month=12,day=10)),(
                datetime.date(year=2001,month=10,day=1),
                datetime.date(year=2001,month=12,day=lastday(2001,12))
            ))

    def test_convenience(self):
        with patch("cartographer.services.today") as mock_today:
            mock_today.return_value = date(year=1999,month=3,day=14)
            self.assertEqual(currentQuarter(),1)
            mock_today.return_value = date(year=2001,month=6,day=14)
            self.assertEqual(currentQuarter(),2)
