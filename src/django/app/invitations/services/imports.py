import os
import logging

from typing import List,Iterable,Dict

import pydantic

from django.conf import settings
from django.core import exceptions, validators
from django.db import IntegrityError

from django.contrib.auth.models import User

import json

from hashlib import md5

from api.models import Country
from invitations.models import CountryAssignment,InvitationRow,Invitation

logger = logging.getLogger(__name__)

# ==============================================
# Data import

def parseInviteFile(lod: Iterable[Dict[str,str]])->List[InvitationRow]:
    NONCOUNTRIES = ["email","position","affiliation","name"]

    first = next(lod)
    countries = [h for h in first.keys() if h not in NONCOUNTRIES]

    def parseRow(row):
        fixval = lambda x: False if "" else x
        ncrow = {k:v for k,v in row.items() if k in NONCOUNTRIES}

        ctries = []
        for key,val in row.items():
            try:
                ctries.append(CountryAssignment(name=key, assigned=val))
            except pydantic.ValidationError:
                pass
        try:
            return InvitationRow(**ncrow,countries = [c.name for c in ctries if c.assigned])
        except pydantic.ValidationError:
            return None

    inviteRows = [parseRow(first)]+[parseRow(r) for r in lod]
    inviteRows = [ir for ir in inviteRows if ir is not None]
    return inviteRows 

def bulkCreateInvites(data: List[InvitationRow], cohort = None)->List[Invitation]:
    res = {"messages":[],"data":{"updated":0,"added":0}}
    for entry in data:
        try:
            User.objects.get(username = entry.email)
        except User.DoesNotExist:
            pass
        else:
            res["messages"].append(f"User {entry.email} already exists")
            continue

        try:
            invitation = Invitation.objects.get(email=entry.email)
        except Invitation.DoesNotExist:
            invitation = Invitation(
                    email = entry.email
                )
            invitation.save()
            res["data"]["added"]+=1
        else:
            res["data"]["updated"]+=1

        invitation.metadata = {"position":entry.position,"affiliation":entry.affiliation}
            
        countries = []
        for cname in entry.countries:
            try:
                c = Country.objects.get(name=cname)
            except Country.DoesNotExist:
                res["messages"].append(f"Did not find country {cname} while creating invite for {entry.email}")
            else:
                countries.append(c)

        invitation.countries.set(countries)
    return res 
