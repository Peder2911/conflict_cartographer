
from django.conf import settings

from django.contrib.auth.models import User
from hashlib import md5

from api.models import Shape

# ==============================================
# Invitation 

def hasDrawn(user):
    drawn = Shape.objects.filter(author = user)
    return len(drawn) > 0

# ==============================================
# Referrals 

def referralKeygen(email):
    salted = email + settings.SECRET_KEY
    return md5(salted.encode()).hexdigest()
