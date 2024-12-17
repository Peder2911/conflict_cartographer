"""
Decorator(s) useful for writing views
"""
#from requests.exceptions import HTTPError
from typing import Callable
import requests
from django.http import HttpResponse

def service_proxy_error(fn:Callable[[any],requests.Response])->Callable[[any],HttpResponse]:
    """
    'Proxies' errors properly when using service-calls to create views.
    """
    def inner(*args,**kwargs):
        try:
            return fn(*args,**kwargs)
        except requests.exceptions.HTTPError as e:
            return HttpResponse(e.response.content,status=e.response.status_code)
    return inner

