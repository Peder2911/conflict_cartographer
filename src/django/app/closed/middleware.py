
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse

def check_active(get_response):
    def middleware(request):

        closed = not settings.ACTIVE
        nonloop = not request.path == "/closed/"
        adminpage = request.path.startswith("/admin/")
        staff = request.user.is_staff

        try:
            if closed and nonloop and not staff and not adminpage: 
                    return redirect("closed")
            return get_response(request)
        except Exception as e:
            return HttpResponse(str(e))
    return middleware

