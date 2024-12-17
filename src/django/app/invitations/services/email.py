"""
Services for dispatching email
"""
import re
import os
from typing import List,Dict,Any
import warnings

import logging

from pydantic import BaseModel,EmailStr,constr

import premailer
import markdown
from premailer import Premailer

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

from invitations.models import EmailTemplate,Invitation
from invitations.util import referralKeygen

from lib.onlyoneactive import OnlyOneActive

logger = logging.getLogger(__name__)
premailer = Premailer(
        cssutils_logging_level=logging.CRITICAL
        )

def renderEmailTemplate(template: EmailTemplate, context: Dict[Any,Any])-> str:
    """
    Renders a HTML message from an EmailTemplate instance
    """
    md = markdown.Markdown()

    if template.htmlMessage is None:
        fixLnBreaks = lambda lines: "".join([x+"<br>" for x in lines.split("\n")])
        context.update({
            "headline": template.headline,
            "content": md.convert(template.message),
            "signature": fixLnBreaks(template.signature)
        })
        html = render_to_string("mail/tpl.html",context)
        warnings.filterwarnings("ignore")
        html = premailer.transform(html)
        template.htmlMessage = html
    else:
        pass
    return template.htmlMessage

def dispatchInvitation(invitation: Invitation)-> bool:
    """
    Sends an email to an invitee
    """
    try:
        assert not invitation.mailed and not invitation.fulfilled
    except AssertionError:
        logger.warning(f"Invitation for {invitation.email} was not sent: "
                        "Already fulfilled!")
        return False

    if invitation.refkey is None:
        invitation.refkey = referralKeygen(invitation.email)
        invitation.save()
    
    if invitation.customemail and invitation.customsig:
        et = EmailTemplate(
                subject = settings.DEFAULT_EMAIL_TITLE,
                headline = "Conflict Cartographer",
                message = invitation.customemail,
                signature = invitation.customsig,
            )
    else:
        try:
            et = EmailTemplate.objects.get(active=True,email_type="inv")
        except EmailTemplate.DoesNotExist:
            et = EmailTemplate.objects.create(
                    active = True,
                    subject = settings.DEFAULT_EMAIL_TITLE,
                    email_type = "inv"
                )

    html = renderEmailTemplate(et,{"link":invitation.invitationLink()})
    plaintext = re.sub("\[[^\)]+",invitation.invitationLink(),et.message)

    call = {
        "subject": et.subject,
        "message": plaintext, 
        "html_message": html,
        "from_email":settings.EMAIL_FROM_ADDRESS,
        "recipient_list":[invitation.email]
    }

    try:
        mail.send_mail(**call)
    except ConnectionRefusedError:
        logger.error("Failed to send email to %s, connection refused!",invitation.email)
        return False
    else:
        logger.info("Sent email to %s",invitation.email)
        invitation.mailed = True
        invitation.save()
        return True
