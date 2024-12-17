
from django.contrib.auth.forms import UserCreationForm 
from django import forms

class ReferredSignupForm(UserCreationForm):
    email = forms.EmailField(max_length = 254)  
    username = forms.CharField(max_length = 254)
