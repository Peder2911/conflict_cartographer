import re
import os
from typing import List

import logging

from pydantic import BaseModel,EmailStr,constr

import markdown
import premailer

from django.conf import settings

from django.template import Template,Context
from django.template.loader import render_to_string

from django.db.models import CharField,Model,OneToOneField,ManyToManyField,TextChoices
from django.db.models import BooleanField,JSONField,EmailField,CASCADE,TextField

from django.contrib.auth.models import User

from django.core import mail 
from django.db.utils import IntegrityError

from django.utils.translation import gettext_lazy

from api.models import Country,Profile

#from invitations.services.email import dispatchInvitation
from invitations.util import referralKeygen

from lib.onlyoneactive import OnlyOneActive

logger = logging.getLogger(__name__)

class Invitation(Model):
    """
    The invitation class
    """
    email = EmailField(unique = True,
            help_text="Email to send invite to")
        
    # Added when user completes registration
    user = OneToOneField(
        User, related_name = "invitation", null = True, blank = True,
        on_delete = CASCADE)

    mailed = BooleanField(default=False,editable=False,
            help_text="Indicates whether or not the invitation has been dispatched, "
                      "that is, if an email has been sent to the target recipient")

    fulfilled = BooleanField(default=False,editable=False, 
            help_text="Indicates whether or not the invitation has been fulfilled, "
                      "meaning a user has been registered for it.")

    metadata = JSONField(default=dict,blank=True,editable=False,
            help_text="Metadata that will be added to the user profile "
                      "once they register. (occupation/sex/age/...) "
                      "<a href='https://en.wikipedia.org/wiki/json' target='_blank'>"
                      "JSON Formatted."
                      "</a>")

    customemail = TextField(verbose_name="Custom invitation email", default = "", 
            blank = True,
            help_text = "A custom email text to send to this particular invitee. "
                        "The text will be pasted into the standard email template, "
                        "which includes the invitation link. If this field is left "
                        "blank, the active email template will be used instead.")

    customsig = TextField(verbose_name="Custom signature", default = "The Conflict Cartographer Team",
            blank = False, null = False,
            help_text = "A custom signature which will be displayed at the bottom"
                        " of the email. The default is \"The Conflict Cartographer Team\".")

    invitedBy = EmailField(verbose_name="Invitation was sent by this user",
            default = "", blank = True, null = True)

    countries = ManyToManyField(Country,related_name="invited_assignees",
            blank = True,
            help_text="Countries that will be assigned to the user "
                      "once they complete registration")

    refkey = CharField(max_length = 32, null = True, editable=False)

    def save(self,*args,**kwargs):
        if self.refkey is None:
            self.refkey = referralKeygen(self.email)

        qs = User.objects.filter(email = self.email)
        if len(qs)>0:
            self.fulfilled = True

        super().save(*args,**kwargs)

    def profile(self,user):
        profile = Profile(
            user = user
        )
        profile.save()
        profile.countries.set(self.countries.all())
        return profile

    def invitationLink(self):
        return os.path.join(settings.INVITATION_LINK_BASE,self.refkey)

    def unsubLink(self):
        return os.path.join(settings.UNSUB_LINK_BASE,self.refkey)

    def __str__(self):
        return f"Invitation for {self.email}"

class EmailTemplate(OnlyOneActive,Model):
    """
    An editable email template which is used to draft invitation emails interactively
    """

    class EmailTypes(TextChoices):
        INVITATION  = "inv", gettext_lazy("invitation")
        REMINDER = "rem", gettext_lazy("reminder")

    subject = CharField(max_length=1024,default=settings.DEFAULT_EMAIL_TITLE,
            help_text="Subject-field of email")

    headline = CharField(
            max_length=1024, 
            help_text="Headline to display in the email", 
            default="Conflict Cartographer"
            )

    message = TextField(default="[{{link}}](Click this link to participate)",
            help_text="Message-body of text. "
                      "<a href='https://en.wikipedia.org/wiki/markdown' target='_blank'>"
                      "Markdown formatted"
                      "</a> "
                      "Do not delete the weird-looking [{{link}}](click me) "
                      "tag!")

    signature = TextField(default="The conflict cartographer team",
            help_text="The signature at the bottom of the email")

    htmlMessage = TextField(
            null=True,
            blank=True,
            editable=False,
            help_text="cached rendered HTML field")

    email_type = CharField(
            max_length=3,
            choices=EmailTypes.choices,
            default=EmailTypes.INVITATION,
            help_text="What kind of email is this? "
                      "Determines when this email is sent.")

    def save(self,*args,**kwargs):
        self.htmlMessage = None
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.email_type} - \"{self.subject}\""

class CountryAssignment(BaseModel):
    name: constr(strip_whitespace=True,regex="^[a-zA-Z -]+$")
    assigned: bool

class InvitationRow(BaseModel):
    position: str
    affiliation: str
    email: EmailStr 
    countries: List[str] 
