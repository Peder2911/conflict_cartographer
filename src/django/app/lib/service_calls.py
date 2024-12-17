"""
Various calls that are vendored by this API, but which depend on other services
for functionality. Essentially just function wrappers for other services.
"""
import os
from typing import Callable,Dict

from datetime import date
import requests
from django.conf import settings
from exceptions import ConfigurationError

def year_span():
    base = date.today()
    return base.replace(month=1,day=1),base.replace(month=12,day=31) 

def ok_or_raise(fn:Callable[[any],requests.Response])->Callable[[any],requests.Response]:
    def inner(*args,**kwargs):
        rq = fn(*args,**kwargs)
        try:
            assert str(rq.status_code)[0] == "2"
        except AssertionError as e:
            raise requests.exceptions.HTTPError("HTTP request did not return 2xx",
                    response=rq) from e
        return rq
    return inner

def json_request(fn:Callable[[any],requests.Response])->Callable[[any],Dict[str,any]]:
    def inner(*args,**kwargs):
        rq = fn(*args,**kwargs)
        try:
            assert rq.headers["Content-Type"] == "application/json"
            data = rq.json()
        except (json.decoder.JSONDecodeError,AssertionError) as e:
            raise AssertionError("API did not return JSON")
        return data
    return inner

def convert_dates(fn: Callable[[any],Dict[str,any]])->Callable[[any],Dict[str,any]]:
    def inner(*args,**kwargs):
        data = fn(*args,**kwargs)
        for k in data:
            try:
                data[k] = date.fromisoformat(data[k])
            except (ValueError,TypeError):
                pass
        return data
    return inner

@convert_dates
@json_request
@ok_or_raise
def span(start: date,end: date,shift: int,frac: int=settings.SCHEDULE_FRAC):
    url = settings.SCHEDULER_URL
    path_elements = (start,end,frac,shift)
    for v in [str(v) for v in path_elements]:
        url += "/"+v
    return requests.get(url)

@convert_dates
@json_request
@ok_or_raise
def span_from_today(shift: int = 0)->requests.Response:
    frac = settings.SCHEDULE_FRAC
    return requests.get(os.path.join(settings.SCHEDULER_URL,"today",str(frac),str(shift)))

def span_of_current_open()->Dict[str,any]:
    current_span = span_from_today()
    duration = current_span["duration_months"]

    try:
        assert duration >= settings.OPEN_MONTHS
    except AssertionError as e:
        raise ConfigurationError("OPEN_MONTHS") from e

    start_of_open = span(current_span["start"],current_span["end"],
            frac=duration,
            shift=duration-settings.OPEN_MONTHS)

    return {
        "start": start_of_open["start"],
        "end": current_span["end"]
    }

def today_is_open()->Dict[str,any]:
    open_span = span_of_current_open()
    today = date.today()
    is_open = (today>=open_span["start"]) & (today <= open_span["end"])
    left_until_open = open_span["start"] - today
    return {
        "open": is_open,
        "opening_date": open_span["start"],
        "closing_date": open_span["end"],
        "days_until_open": left_until_open.days,
    }
