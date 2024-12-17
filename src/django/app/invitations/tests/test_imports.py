import csv
import io
import pickle

import unittest
from typing import Dict
import hashlib

import re

from bs4 import BeautifulSoup

from django.core import mail
from django.test import TestCase,Client

from django.core.files.base import ContentFile

from django.conf import settings
from django import urls

from django.contrib.auth.models import User

from invitations.models import Invitation,EmailTemplate
from invitations.util import referralKeygen
from invitations.services.imports import bulkCreateInvites,parseInviteFile
from api.models import Country

EXAMPLE_CSV = [
    "name,email,position,affiliation,one,two,thr,fou,fiv,six,sev,eig",
    "name nameson,one@one.com,plumber,Somewhere,1,1,1,1,1,0,0,0",
    "name nameson,two@two.com,cleaner,Someplace,0,0,0,1,1,1,1,1",
    "name nameson,thr@thr.com,cleaner,Somewhere,1,1,1,1,1,0,0,0",
    "name nameson,fou@fou.com,plumber,Somewhere,0,0,0,1,1,1,1,1",
    "name nameson,fiv@fiv.com,cleaner,Someplace,1,1,1,1,1,0,0,0",
]


class InvitationTest(TestCase):
    serialized_rollback = True
    def test_parse(self):
        """
        Tests parsing an invite-csv
        """
        f = io.StringIO("\n".join(EXAMPLE_CSV))
        reader = csv.DictReader(f)
        parsed = parseInviteFile(reader)

        f.seek(0)
        reader = csv.DictReader(f)
        rows = [*reader]
        self.assertEqual(len(parsed),len(rows))

        for v in ("email","affiliation","position"):
            self.assertEqual(
                    [getattr(r,v) for r in parsed],
                    [r[v] for r in rows]
                )

    def test_bulk_add(self):
        for i,c in enumerate(("Colombia","Syria","Mali")):
            ctry = Country(name = c, shape = {}, simpleshape = {}, iso2c = c[:2],gwno = i)
            ctry.save()

        User.objects.create_superuser(username="admin",password="admin")
        self.client.login(username="admin",password="admin")
        data = [
            {"email":"a@b.com","affiliation":"a","position":"a",
                "Colombia":1,"Syria":0,"Mali":0},
            {"email":"b@c.com","affiliation":"b","position":"a",
                "Colombia":0,"Syria":1,"Mali":0},
            {"email":"c@d.com","affiliation":"a","position":"b",
                "Colombia":0,"Syria":0,"Mali":1},
            {"email":"d@e.com","affiliation":"a","position":"c",
                "Colombia":0,"Syria":1,"Mali":1},
            {"email":"e@f.com","affiliation":"b","position":"a",
                "Colombia":1,"Syria":0,"Mali":0},
        ]

        f = io.StringIO()
        writer = csv.DictWriter(f,fieldnames=data[0].keys())
        writer.writeheader()
        for r in data:
            writer.writerow(r)
        cf = ContentFile(f.getvalue().encode())

        postData = {
                "title":"myexperts.csv",
                "datafile":ContentFile(f.getvalue().encode())
            }

        r = self.client.post(urls.reverse("uploadexcel"),postData,follow=True)
        self.assertEqual(r.status_code,200)

        self.assertEqual(Invitation.objects.count(),5)

        self.assertTrue("Colombia" in [c.name for c in Invitation.objects.get(email="a@b.com").countries.all()])
        self.assertTrue("Colombia" not in [c.name for c in Invitation.objects.get(email="b@c.com").countries.all()])
