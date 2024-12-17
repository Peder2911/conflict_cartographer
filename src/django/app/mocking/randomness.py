
import random
from toolz import compose
from datetime import datetime, date, timedelta

def minus_random_days(x):
    return x - timedelta(days = int(random.random() * 365))

random_past_date = compose(minus_random_days, date.today)
random_past_time = compose(minus_random_days, datetime.now)
