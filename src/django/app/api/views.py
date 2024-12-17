import json
from datetime import datetime,date
from collections import defaultdict
from typing import Literal

import pydantic

import geojson

from django.http import HttpResponse,HttpRequest,JsonResponse
from django.shortcuts import render,redirect

from django.db.models.query import QuerySet
from django.utils import timezone

from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_http_methods

from django.conf import settings

from rest_framework import viewsets, status, exceptions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions

from api import models
from api.models import Shape,Feedback
from api.models import Country,ProjectDescription,WaiverText,NonAnswer

from cartographer.services import currentQuarter,currentYear,quarterRange
from api.validation import CountryFeatureCollection
from api.forms import ProfileForm
from api.view_decorators import service_proxy_error

from lib import service_calls

# ================================================
# Utility views 

@login_required
def whoami(request):
    """
    Returns stored information about the user
    """
    return JsonResponse({"name": request.user.username, "waiver": request.user.profile.waiver})

# ================================================
# Countries 
     
class CountryMetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Country
        fields = ["url","name","gwno","iso2c"]

class CountryShapeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Country
        fields = ["url","shape","name","iso2c","gwno"]

class CountryViewSet(viewsets.ModelViewSet):
    """
    Yields shape in detail view.
    """
    queryset = models.Country.objects.filter(active=True)
    serializer_class = CountryMetaSerializer  
    #permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CountryShapeSerializer
        else:
            return CountryMetaSerializer

# ================================================
# Shape

class ShapeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shape
        fields = ["url","country","shape","values","author","date"]

    def validate_shape(self,value):
        try:
            gjf = geojson.Feature(type= "Feature", geometry = value,properties = dict())
        except ValueError as e:
            raise serializers.ValidationError
        if not gjf.is_valid:
            raise serializers.ValidationError
        return value
    
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date = serializers.DateField(read_only=True,default=date.today)

class ShapeViewSet(viewsets.ModelViewSet):
    """
    Application API used to communicate with participants.
    The viewset adds the request user as author of each shape.
    The viewset is also restricted by quarter, meaning only shapes from the
    current quarter are returned.
    """
    serializer_class = ShapeSerializer  
    filterset_fields = ["country"]
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        s,e = quarterRange()
        return Shape.objects.filter(author = self.request.user, date__gte=s,date__lte=e) 

# ================================================
# Feedback
class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback 
        fields = ["url","message","stars","author","date"]
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date = serializers.DateField(read_only=True,default=date.today)

class FeedbackViewset(viewsets.ModelViewSet):
    """
    Viewset that lets anyone post, but only lets admin users GET feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def list(self,*args,**kwargs):
        if self.request.user.is_staff:
            return super().list(self,*args,**kwargs)
        else:
            return Response(status=401)

    def retrieve(self,*args,**kwargs):
        if self.request.user.is_staff:
            return super().retrieve(self,*args,**kwargs)
        else:
            return Response(status=401)

# ================================================
# Project views

def get_fulfilled_projects(user):
    period_start, period_end = quarterRange()
    
    shapes = Shape.objects.filter(author=user,date__gte=period_start,date__lte=period_end)
    nonAnswers = NonAnswer.objects.filter(author=user,date__gte=period_start,date__lte=period_end)
    return {sh.country for sh in shapes}.union({na.country for na in nonAnswers})

def get_pending_projects(user):
    projects = (Country
            .objects
            .filter(assignees=user.profile)
        )
    return set(projects).difference(get_fulfilled_projects(user))

def next_project(request:HttpRequest)->HttpResponse:
    pending = get_pending_projects(request.user)
    if len(pending)>0:
        next_project = pending.pop()
        serialized = CountryShapeSerializer(next_project,context={"request":request}).data
        return JsonResponse({"status":"active","next":serialized})
    else:
        return JsonResponse({"status":"finished","next":False})

def pending_projects(request:HttpRequest)->HttpResponse:
    pending = get_pending_projects(request.user)
    serialized = CountryMetaSerializer(pending,many=True,context={"request":request}).data
    return JsonResponse({"countries":serialized})

def fulfilled_projects(request:HttpRequest)->HttpResponse:
    pending = get_fulfilled_projects(request.user)
    serialized = CountryMetaSerializer(pending,many=True,context={"request":request}).data
    return JsonResponse({"countries":serialized})

#@api_view(("GET","POST",))
def projects(request:HttpRequest)->HttpResponse:
    """
    Get list of countries assigned to current user.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"status":"error","message":"not authenticated"},status=403)

    if request.method == "GET":
        try:
            countries = Country.objects.filter(assignees = request.user.profile)
            serialized = CountryMetaSerializer(countries,many=True,context={"request":request}).data
            return JsonResponse({"countries":serialized})
        except Exception as e:
            return JsonResponse({"message":str(e)},status=500) 

    elif request.method == "POST":
        if request.headers["Content-Type"] == "application/json":
            data = json.loads(request.body)
        else:
            return JsonResponse({"status":"error"},415)

        try:
            selected = data["selected"]
        except KeyError:
            return HttpResponse(status=400)

        profile = request.user.profile
        countries = Country.objects.filter(name__in=data["selected"])
        profile.countries.set(countries)
        profile.save()

        return HttpResponse(status=205)

    else:
        return JsonResponse({"status":"error"},status=405)

@api_view(("GET",))
def unfulfilled(request:HttpRequest)->HttpResponse:
    """
    Get a list of the countries not currently fulfilled by the user
    """
    try:
        period_start, period_end = quarterRange()

        def has_answered(c:Country):
            n_shapes = Shape.objects.filter(
                    author=request.user,
                    country=c,
                    date__gte=period_start,date__lte=period_end).count()
            nonanswers = NonAnswer.objects.filter(author=request.user, country=c, date__gte=period_start,date__lte=period_end).count()
            return (n_shapes > 0 or nonanswers > 0)

        countries = (Country
                .objects
                .filter(assignees__pk=request.user.profile.pk)
            )

        countries = [c for c in countries if not has_answered(c)]
        serialized = CountryMetaSerializer(countries,many=True,context={"request":request}).data
        return JsonResponse({"countries":serialized})
    except Exception as e:
        return Response(str(e),status=500)


def projectInfo(request:HttpRequest,verbose=False):
    """
    Returns the currently active project text.
    """
    #verbose = request.GET.get("verbose","false") == "true"
    project = ProjectDescription.objects.filter(active=True).first()
    if project is None:
        data = {"status":"error",
                "title":"Missing",
                "description":"No project has been defined yet!"}
    else:
        description = project.long_description if verbose else project.description
        data = {"status":"ok",
                "title":project.title,
                "description":description}
    return JsonResponse(data)

def waiver(request:HttpRequest)->HttpResponse:
    """
    Endpoint for recieving accept / reject on the user data waiver (POST), and
    for returning the waiver text (GET).
    """
    if request.method == "GET":
        try:
            wt = WaiverText.objects.filter(active=True).first().content
        except Exception as e:
            wt = f"No waiver text defined! ({str(e)})"
        return JsonResponse({"status":"ok","message":wt})
    elif request.method=="POST":
        try:
            data = json.loads(request.body)
            agreed = data["agree"]
        except (json.decoder.JSONDecodeError,KeyError):
            return HttpResponse(status=400)
        if agreed:
            request.user.profile.waiver = True
            request.user.profile.save()
            return JsonResponse({"status":"ok","message":"Thanks"})
        else:
            return JsonResponse({"status":"ok","message":"Did not agree"})
    else:
        return HttpResponse(status=405)

@require_http_methods(["POST"])
def updateCountries(request):
    """
    Updating the countries available to the system.
    """

    if not request.user.is_staff:
        return JsonResponse({"status":"error","messages":"permission denied"},status=status.HTTP_403_FORBIDDEN)

    class CountryDataUpload(pydantic.BaseModel):
        small: CountryFeatureCollection 
        large: CountryFeatureCollection
    try:
        uploaded = CountryDataUpload(**json.loads(request.body.decode()))
        getCountries = lambda fc: {c.properties.CNTRY_NAME for c in fc.features}
        assert len(uploaded.small.features) == len(uploaded.large.features)
        assert getCountries(uploaded.small) == getCountries(uploaded.large)
    except Exception as e:
        return JsonResponse({"status":"error","messages":str(e)},status=status.HTTP_400_BAD_REQUEST)

    saved = 0
    updated = 0

    for small,large in zip(uploaded.small.features,uploaded.large.features):
        try:
            c = Country.objects.get(gwno = small.properties.GWCODE)
        except Country.DoesNotExist:
            c = Country(
                    gwno = small.properties.GWCODE,
                    name = small.properties.CNTRY_NAME,
                    iso2c = small.properties.ISO1AL2,
                    shape = dict(large.geometry),
                    simpleshape = dict(small.geometry)
                )
            saved += 1
        else:
            c.iso2c = small.properties.ISO1AL2
            c.name = small.properties.CNTRY_NAME
            c.shape = dict(large.geometry)
            c.simpleshape = dict(small.geometry)
            updated += 1
        c.save()

    return JsonResponse({"status":"success","saved":saved,"updated":updated})

def profile_meta(request:HttpRequest)->HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(status=403)
    
    if request.method=="GET":
        data = request.user.profile.meta
        return JsonResponse(data)

    elif request.method=="POST":
        if request.headers["Content-Type"] == "application/json":
            data = json.loads(request.body)
        else:
            return HttpResponse(status=415)
    else:
        return HttpResponse(status=405)

    try:
        formatted = {q["title"]:q["value"] for q in data}
    except KeyError:
        return HttpResponse(status=400)

    request.user.profile.meta = formatted
    request.user.profile.save()
    return HttpResponse(status=205)


def editProfile(request:HttpRequest)->HttpResponse:
    """
    Updating the metadata associated with each user.
    """
    if request.method == "GET":
        profile = request.user.profile
        form = ProfileForm(profile.meta)
        return render(request,"registration/editprofile.html",{"form":form})
    elif request.method =="POST":
        data = ProfileForm(request.POST)
        if data.is_valid():
            request.user.profile.meta = data.cleaned_data
            request.user.profile.save()
            return redirect("/")
    else:
        return HttpResponse(status=405)

def hasProfile(request:HttpRequest)->HttpResponse:
    """
    Simple Y/N on whether or not user has registered a profile.
    """
    return JsonResponse({"status":"ok","profile":bool(request.user.profile.meta)})

def projectChoices(request:HttpRequest)->HttpResponse:
    """
        Get all projects
    """
    if request.method == "GET":
        projects = CountryViewSet().get_queryset().exclude(assignees__pk = request.user.profile.pk)
        projects = [{"name":c.name,"pk":c.pk} for c in projects]
        return JsonResponse({"status":"ok","projects":projects})
    else:
        return HttpResponse(status=405)

@require_http_methods(["POST"])
def editProjects(request:HttpRequest,action:Literal["add","remove"])->HttpResponse:
    """
    Endpoint for adding / removing projects from the currently assigned
    projects field for the current user.
    """
    try:
        data = json.loads(request.body)
        country = Country.objects.get(pk=data["pk"])
        prof = request.user.profile
        if action in ["add","remove"]:
            getattr(prof.countries,action)(country)
            prof.save()
        else:
            return HttpResponse(status=404)

    
    except Exception as e:
        return JsonResponse({"status":"error","message":str(e)},status=500)
    else:
        return JsonResponse({"status":"ok"})

def calendar(request:HttpRequest)->HttpResponse:
    """ 
    Returns the server time information used by the server to timestamp
    answers.  
    """
    s,e = quarterRange()
    return JsonResponse({
        "status":"ok",
        "quarter": currentQuarter(),
        "year": currentYear(),
        "starts": str(s),
        "ends": str(e)
    })

@require_http_methods(["POST"])
def nonanswer(request:HttpRequest,project:int)->HttpResponse:
    """
    Endpoint for toggling nonanswer status for a given project.
    """
    try:
        country = Country.objects.get(pk=project) 
    except Country.DoesNotExist:
        return HttpResponse(status=404)

    s,e = quarterRange()
    try:
        na = NonAnswer.objects.get(
                
                author=request.user,
                country=country,
                date__gte=s,
                date__lte=e)
    except NonAnswer.DoesNotExist:
        na = NonAnswer(author=request.user,country=country)
        na.save()
        return JsonResponse({"status":"ok","nonanswer":True})
    else:
        na.delete()
        return JsonResponse({"status":"ok","nonanswer":False})

def projectStatus(request: HttpRequest, project: int)->HttpResponse:
    """
    Returns current status on a project for a user.
    Used to display details about project progression.
    """

    if not request.user.is_authenticated:
        return HttpResponse(status=403)

    try:
        country = Country.objects.get(pk=project) 
    except Country.DoesNotExist:
        return HttpResponse(status=404)

    s,e = quarterRange()
    shapes = Shape.objects.filter(
            author = request.user, 
            country = country, 
            date__gte=s,date__lte=e).count()

    try:
        NonAnswer.objects.get(
                author=request.user,country=country,
                date__gte = s, date__lte=e
                )
    except NonAnswer.DoesNotExist:
        na = False
    else:
        na = True

    return JsonResponse({
            "shapes": shapes,
            "nonanswer": na
        })

def clearShapes(request: HttpRequest, project: int)->HttpResponse:
    """
    Clear all shapes for a project.
    """
    try:
        country = Country.objects.get(pk=project) 
    except Country.DoesNotExist:
        return HttpResponse(status=404)

    s,e = quarterRange()
    shapes = Shape.objects.filter(
            author = request.user,
            country = country,
            date__gte = s,
            date__lte = e)
    d = len(shapes)
    
    shapes.delete()
    return JsonResponse({"status":"ok","deleted":d})

@service_proxy_error
def get_current_quarter(request:HttpRequest,shift=0)->HttpResponse:
    data = service_calls.span_from_today(shift=shift)
    return JsonResponse(data)

@service_proxy_error
def is_open(request:HttpRequest)->HttpResponse:
    return JsonResponse(service_calls.today_is_open())
