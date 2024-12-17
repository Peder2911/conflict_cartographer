
import logging
from hashlib import sha256
from django.http import HttpRequest
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.conf import settings

from api.models import Profile

logger = logging.getLogger(__name__)

def salt_and_hash(value: str):
    return sha256((settings.SECRET_KEY + value).encode()).hexdigest()


def scrub_profile(profile: Profile)-> Profile:
    """
    scrub_profile
    =============
    parameters:
        profile (api.models.Profile)
    returns
        (api.models.Profile): A profile with all person-identifiable data
                              erased
    """
    profile.meta = {}
    return profile

def scrub_user(user: User)-> User:
    """
    scrub_user
    ==========
    
    parameters:
        user (django.contrib.auth.models.User)
    returns:
        (django.contrib.auth.models.User): A user object with all
                                           person-identifiable data erased.
    """
    user.profile = scrub_profile(user.profile)

    user.email = ""
    
    for attribute in ("username", "first_name", "last_name"):
        val = getattr(user, attribute)
        if val:
            setattr(user, attribute, salt_and_hash(val))

    if User.objects.filter(username = user.username).exists():
        user = scrub_user(user)

    user.is_active = False

    return user

def scrub_users(model_admin: "UserAdmin", request: HttpRequest, queryset):
    for user in queryset:
        user = scrub_user(user)
        user.profile.save()
        user.save()

scrub_users.short_description = "Remove all person-identifiable data from selected users."

class ProfileInline(admin.StackedInline):
    model = Profile 

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (
            ProfileInline,
        )
    actions = [scrub_users]

