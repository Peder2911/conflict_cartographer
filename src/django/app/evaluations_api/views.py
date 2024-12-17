from functools import partial
from toolz.functoolz import curry

from django.http import JsonResponse ,HttpRequest, HttpResponse
from django.conf import settings
from django.urls import path,register_converter

from evaluations_api import api,exceptions
from api.models import Country

scheduler = api.Scheduler(settings.SCHEDULER_URL)

ged = api.Ged(settings.SCHEDULER_URL, settings.GED_URL)
preds = api.Preds(settings.SCHEDULER_URL, settings.API_URL)
metrics = api.Metrics(settings.SCHEDULER_URL, settings.METRICS_URL)

countries = api.Countries(settings.API_URL)

def with_request_user(fn,request):
    return partial(fn,user=request.user.id)

def only_allowed(fn):
    def inner(*args,**kwargs):
        try:
            return fn(*args,**kwargs)
        except exceptions.NotAllowed:
            return HttpResponse(status=403)
    return inner

class NegativeIntConverter:
    regex = r"-?\d+"
    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%d" % value

register_converter(NegativeIntConverter,"nint")

urls = []

def me(request):
    return JsonResponse({"uid":request.user.id})

urls.append(path("whoami/",me))

def ged_points(_:HttpRequest, country: int, shift:str):
    return JsonResponse(ged.points(country,shift))

urls.append(path("ged/points/<int:country>/<nint:shift>/",ged_points))

def ged_buffered(_:HttpRequest, country: int, shift:str):
    return JsonResponse(ged.buffered(country,shift))

urls.append(path("ged/buffered/<int:country>/<nint:shift>/",ged_buffered))

@only_allowed
def list_preds(request:HttpRequest, country, shift):
    return JsonResponse(
            with_request_user(preds.list,request)(country=country,shift=shift)
        )

urls.append(path("countries/<int:country>/preds/<nint:shift>/",list_preds))

@only_allowed
def prediction_detail(request:HttpRequest, pred_id):
    return JsonResponse(
            with_request_user(preds.detail,request)(shape_id=pred_id)
        )

urls.append(path("preds/<int:pred_id>/",prediction_detail))

def overall_summary(request:HttpRequest):
    handler = curry(metrics.overall,request.user.id)
    return JsonResponse(handler(shift=request.GET.get("shift")))

urls.append(path("summary/",overall_summary))

@only_allowed
def available_summaries(request:HttpRequest):
    handler = curry(metrics.available,request.user.id)
    return JsonResponse({"countries":handler(shift=request.GET.get("shift"))})

urls.append(path("countries/",available_summaries))

@only_allowed
def country_summary(request:HttpRequest,gwno:int):
    handler = curry(metrics.country)(request.user.id)
    data = handler(gwno,shift=request.GET.get("shift"))
    data["gwno"] = gwno
    data["name"] = Country.objects.get(gwno = gwno).name 
    return JsonResponse(data)

urls.append(path("countries/<int:gwno>/",country_summary))
