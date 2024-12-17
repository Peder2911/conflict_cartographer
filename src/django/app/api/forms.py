
from django.forms import Form,CharField,IntegerField

class ProfileForm(Form):
    profession = CharField(label="Profession",max_length=100, required=False)
    affiliation = CharField(label="Institutional affiliation",max_length=100, required=False)
