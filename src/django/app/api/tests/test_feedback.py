
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class FeedbackTest(TestCase):
    def setUp(self):
        self.u = User.objects.create_user(username="chatty",password="chatty")
    def test_giving_feedback(self):
        url = reverse("feedback-list")+"?format=json"
        validFeedback = {"message":"Great work!!","stars":5}
        invalidFeedback = {"foo":"bar"}

        r = self.client.post(url,data=validFeedback,content_type="application/json")
        self.assertEqual(r.status_code,403)

        self.client.login(username="chatty",password="chatty")
        r = self.client.post(url,data=validFeedback,content_type="application/json")
        self.assertEqual(r.status_code,201)

        r2 = self.client.post(url,data=invalidFeedback,content_type="application/json")
        self.assertEqual(r2.status_code,400)

        r3 = self.client.post(url,data="fail",content_type="text")
        self.assertEqual(r3.status_code,415)



