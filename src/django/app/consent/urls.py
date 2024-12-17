
from django.urls import path
from consent import views

urls = [
        path("consent", views.consent),
        path("consent/submit", views.submit_consent)
        ]
