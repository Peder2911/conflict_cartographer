import json

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect
from  django.conf import settings
#from .models import DrawnShape

# Create your views here.

manifest = {
    "name":"Conflict-Cartographer",
    "author":"pedlan@prio.org",
    "version":"0.1",
    "display":"standalone",
    "description":"A data collection app",
}

def cartographer(request):
    if request.user.is_authenticated:
        context = {"manifest":json.dumps(manifest)} 
        return render(request,"cartographer/index.html",context)
    else:
        return redirect("accounts/login")
