"""djangoexplore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, register_converter

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

# MAIN
from cartographer.views import cartographer
import api.urls
from api.admin_views import router as api_admin_router
import invitations.urls
from closed.views import closed
from evaluations_api.views import urls as evaluations_api_urls
from user_administration.urls import urls as user_administration_urls
from consent.urls import urls as consent_urls
from unsubscribe.urls import urlpatterns as unsubscribe_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", cartographer, name = "conflictcartographer"), # MAIN
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path("accounts/",include("django.contrib.auth.urls")),

    path("test/ref/",lambda r: render(r,"django_registration/registration_form.html",{"form":UserCreationForm(),
        "msg":"Welcome {invitation.email}! Please complete your registration to participate."})),
    path("test/reg/",lambda r: render(r,"django_registration/registration_form.html",{"form":UserCreationForm()})),
    path("test/redir/",lambda r: render(r,"django_registration/registration_complete.html",{"form":UserCreationForm()})),
    path("test/login/",lambda r: render(r,"registration/login.html",{"form":AuthenticationForm()})),

    path("closed/",closed,name="closed"),

    path("api/eval/", include(evaluations_api_urls)),
]

urlpatterns += api.urls.urlpatterns
urlpatterns += invitations.urls.urlpatterns
urlpatterns += user_administration_urls
urlpatterns += consent_urls
urlpatterns += unsubscribe_urls 

urlpatterns += [path("aapi/",include(api_admin_router.urls))]
