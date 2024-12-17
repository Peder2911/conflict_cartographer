
from django.test import TestCase
from django.contrib.auth.models import User

from invitations.models import Invitation

class TestReferralPage(TestCase):
    def test_referral_redirect(self):
        """
        This just tests that the referral page doesn't "trap"
        already registered users.
        """
        i = Invitation.objects.create(email="test@test.com")
        u = User.objects.create_user(username="ref",password="ref",email="test@test.com")

        r = self.client.get(i.invitationLink(),follow=True)
        url,_ = r.redirect_chain[-1]
        self.assertNotEqual(url,"/")
        self.assertEqual(r.status_code,200)

        self.client.login(username="ref",password="ref")
        r = self.client.get(i.invitationLink(),follow=True)
        url,_ = r.redirect_chain[-1]
        self.assertEqual(url,"/")
        #self.assertEqual(r.status_code,302)
