
from invitations.views import share
from invitations.models import Invitation
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.core import mail

class TestSharing(TestCase):
    def setUp(self):
        credentials = {"username":"share","password":"share"}
        self.u = User.objects.create_user(**credentials)
        self.client.login(**credentials)

    def test_share(self):
        self.assertTrue(True)

        r = self.client.post(reverse("share"),data={
            "email": "hello@world.com",
            "message": ""
        }, content_type="application/json")

        self.assertEqual(r.status_code,200)

        try:
            i = Invitation.objects.get(email="hello@world.com")
        except Exception as e:
            self.fail(e)

        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[0].to,["hello@world.com"])
