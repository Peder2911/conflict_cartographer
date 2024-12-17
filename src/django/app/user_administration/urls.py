
from django.urls import path
from user_administration.views import delete_me

urls = [
        path("api/profile/deleteme/",delete_me)
    ]
