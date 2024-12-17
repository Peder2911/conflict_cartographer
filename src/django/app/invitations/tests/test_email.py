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
from invitations.services.email import dispatchInvitation
from api.models import Country


class InvitationTest(TestCase):
    serialized_rollback = True

    def test_dispatch_and_register(self):
        """
        Long-form test that tests creating and sending an invite, and then
        registering a user by following the referral link in the invitation email.
        """
        countries = [Country(gwno=i,name=str(i),shape={},simpleshape={}) for i in range(5)]
        for c in countries:
            c.save()

        i = Invitation(email="name@loc.com")
        i.save()
        i.countries.set(countries)
        dispatchInvitation(i)

        m = mail.outbox[0]

        # Mailed flag
        self.assertTrue(i.mailed)

        # Email has proper title
        self.assertEqual(m.subject, settings.DEFAULT_EMAIL_TITLE)

        # Email contains ref. key
        self.assertIsNotNone(re.search(i.refkey,m.body))

        r = self.client.get(i.invitationLink(),follow=True)
        location,*_ = r.redirect_chain[-1]

        soup = BeautifulSoup(r.content,features="html.parser")

        regform = soup.find("form")
        usernameInput = regform.find("input",attrs={"name":"username"})

        # Email is in the username form
        self.assertEqual(usernameInput["value"],i.email)

        url = regform.action if regform.action else location 
        method = regform.method if regform.method else "POST"


        getattr(self.client,method.lower())(url,{
                "username": usernameInput["value"],
                "password1": hashlib.md5(b"1234").hexdigest(),
                "password2": hashlib.md5(b"1234").hexdigest()
            })

        # User was created 
        try:
            u = User.objects.get(email = i.email)
        except User.DoesNotExist:
            self.fail("User was not created")


        # Make sure all countries were added
        self.assertEqual(
                {c.pk for c in countries},
                {c.pk for c in u.profile.countries.all()}
            )

    def test_admin_dispatch(self):
        """
        Tests admin action to send email to selected invites
        """
        user = User.objects.create_superuser(username="admin",email="admin@admin.com",password="admin")
        self.client.login(username="admin",password="admin")

        invites = [Invitation(email=f"{i}@{i}.com") for i in range(5)]
        for i in invites:
            i.save()

        url = urls.reverse("admin:invitations_invitation_changelist")
        data = {'action': 'dispatch_invitation',
                '_selected_action': [i.pk for i in invites]}

        r = self.client.post(url,data,follow=True)
        self.assertEqual(r.status_code,200)
        self.assertEqual(len(invites),len(mail.outbox))

class TestEmailRendering(TestCase):
    def test_rendered_email(self):
        et = EmailTemplate(
                active=True,
                subject="An invitation",
                message="""
# You are hereby invited to my survey

Please fill it out!

[here]({{link}})

Best regards
The Team
                """)
        et.save()
        inv = Invitation(email="name@nameson.com")
        dispatchInvitation(inv)
        self.assertEqual(len(mail.outbox),1)
        m = mail.outbox[0]
        with open("/tmp/m.pckl","wb") as f:
            pickle.dump(m,f)
        self.assertEqual(m.subject,et.subject)
        self.assertIsNotNone(re.search(inv.refkey,m.body))
        self.assertIsNotNone(re.search(
            "You are hereby invited to my survey",
            m.body))

    def test_custom_invite_text(self):
        et = EmailTemplate.objects.create(
                active = True,
                subject = "Inv",
                message = "Please join my survey"
                )

        inv = Invitation.objects.create(
                email = "yee@haw.com",
                customemail = "Hey yee! Please join my survey",
                customsig = "Sincerely, Haw."
                )

        dispatchInvitation(inv)
        self.assertEqual(len(mail.outbox),1)
        m = mail.outbox.pop()
        for msg,mtype in m.alternatives:
            if mtype == "text/html":
                self.assertIsNotNone(re.search("Hey yee! Please join my survey",msg))
                self.assertIsNotNone(re.search(inv.refkey,msg))
                self.assertIsNotNone(re.search("Sincerely, Haw",msg))
