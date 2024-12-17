from django.conf import settings
from django.shortcuts import redirect,render

def closed(request):
    if settings.ACTIVE:
        return redirect("/")
    else:
        return render(request,"closed/closed.html",{})
