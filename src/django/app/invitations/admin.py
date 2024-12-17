from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User,Group

from invitations.models import Invitation,EmailTemplate
from invitations.services.email import dispatchInvitation
from api.models import Profile

# Register your models here.
admin.site.unregister(Group)

def makeLink(url, text=None):
    if text is None:
        text = url
    return f"<p><b><a href={url}>{text}</a></b></p>"

def dispatch_invitation(modeladmin, request, queryset):
    """
    Send invitation email
    """
    for invitation in queryset:
        dispatchInvitation(invitation)

dispatch_invitation.short_description=dispatch_invitation.__doc__

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    exclude = [
        "user",
        "refkey",
        "reached",
        "opened",
        "registered",
    ]

    readonly_fields =[
        "referral_link",
    ]

    list_display = ("email","mailed","fulfilled","ncountries","customized","invitedBy")

    def ncountries(self,obj):
        return len(obj.countries.all())
    ncountries.__doc__ = "Number of countries assigned"

    def customized(self,obj):
        return bool(obj.customemail)
    customized.__doc__ = "Personalized email"

    actions = [dispatch_invitation]
    
    def referral_link(self,obj):
        try:
            url = reverse("referral",args=[obj.refkey])
            link = makeLink(url)
            fieldvalue = link
        except:
            fieldvalue = "-"
        return format_html(fieldvalue)

def makeInvitationLink(inv):
    url = f"{reverse('admin:index')}core/invitation/{inv.pk}"
    return f"<p><a href=\"{url}\">{str(inv)}</a></p>"

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display=("subject","active","email_type")
    readonly_fields=["preview"]

    def preview(self,obj):
        return mark_safe(f'<a href="/admin/invitations/emailpreview/{obj.pk}/" target="_blank">Click to preview</a>')
