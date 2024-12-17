
from django import http
from django.contrib import auth
from django.shortcuts import redirect
from user_administration.admin import scrub_user

def delete_me(request: http.HttpRequest)-> http.HttpResponse:
    if request.user.is_superuser:
        return http.HttpResponse(status = 418)
    elif request.user.is_authenticated:
        user = scrub_user(request.user)
        user.profile.save()
        user.save()
        auth.logout(request)
        return http.HttpResponse(status = 203) 
    else:
        return http.HttpResponse(status = 403)
