import io
import csv
import json

import pydantic

from django.shortcuts import render, redirect

from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required 

from django.db import IntegrityError

from django.views.decorators.http import require_http_methods

from django.http import HttpResponse,HttpRequest,JsonResponse
from invitations.models import Invitation,EmailTemplate
from invitations.services.imports import parseInviteFile,bulkCreateInvites
from invitations.services.email import dispatchInvitation,renderEmailTemplate

def referralRedirect(request,refkey):

    if request.user.is_authenticated:
        return redirect("/")

    try:
        Invitation.objects.get(refkey = refkey)
    except Invitation.DoesNotExist:
        return HttpResponse(status = 404)
    else: 
        request.session["invitation"] = refkey
        return redirect("referralSignup")

def referralSignup(request):
    refkey = request.session.get("invitation",False)

    if request.user.is_authenticated:
        return redirect("/")

    if not refkey:
        return HttpResponse(status = 403)

    try:
        invitation = Invitation.objects.get(refkey = refkey)
    except Invitation.DoesNotExist:
        return redirect("/")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        form.fields["username"].initial = invitation.email
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(username = username, password = raw_password)
            profile = invitation.profile(user)
            profile.save()

            user.email = invitation.email

            invitation.fulfilled = True
            invitation.save()
            #invitation.delete()
            user.save()

            login(request,user)
            return redirect("/") 
    else: 
        form = UserCreationForm()
        form.fields["username"].initial = invitation.email

    # And then
    return render(request, "django_registration/registration_form.html",
            {"form":form,"msg":f"Welcome {invitation.email}! Please complete your registration to participate."})

@require_http_methods(["POST"])
def handleExcelFile(request: HttpRequest)->HttpResponse:
    if not request.user.is_staff:
        return JsonResponse({"status":"error","messages":"permission denied"},status=403)
    try:
        datafile = request.FILES["datafile"]
    except KeyError:
        return JsonResponse({"status":"error","messages":"no file included"},status=400)

    lines = io.StringIO(datafile.read().decode())
    reader = csv.DictReader(lines)
    try:
        lines = parseInviteFile(reader)
    except pydantic.ValidationError as e:
        return JsonResponse({"status":"error","messages":str(e)})

    res = bulkCreateInvites(lines)
    res.update({"status":"success"})
    return JsonResponse(res)

def fileuploadMenu(request:HttpRequest)->HttpResponse:
    return render(request,"invitations/fileuploadMenu.html",{})

def emailpreview(request:HttpRequest,pk:int)->HttpResponse:
    tpl = EmailTemplate.objects.get(pk=pk)
    tpl.htmlMessage = None
    tpl.save()
    return HttpResponse(renderEmailTemplate(tpl,{}))

@login_required
def share(request: HttpRequest)->HttpResponse:
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status":"error","errors":"failed to decode request data"},status=401)

    try:
        sender = request.user.email if request.user.email else None
        reciever = data["email"]
        msg = data["message"] if data["message"] else ""
    except Exception as e:
        return JsonResponse({"status":"error","errors":str(e)},status=401)
    
    try:
        invitation = Invitation.objects.create(email=reciever,invitedBy=sender, customemail = msg)
    except IntegrityError:
        try:
            invitation = Invitation.objects.get(email=reciever)
            invitation.invitedBy = sender
            invitation.customemail = msg
            invitation.save()
            dispatchInvitation(invitation)
            return JsonResponse({"status":"ok","message":"User was already invited!"},status=200)
        except Exception as e:
            return JsonResponse({"status":"error","message":str(e)},status=401)
    else:
        dispatchInvitation(invitation)
        return JsonResponse({"status":"ok","message":"invitation sent"},status=200)
