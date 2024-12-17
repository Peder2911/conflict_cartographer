import base64
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

def has_consented(get_response):
    def middleware(request: HttpRequest) -> HttpResponse:
        has_consented = request.COOKIES.get("privacy-consent") is not None
        nonloop = not request.path.startswith("/consent")
        adminpage = request.path.startswith("/admin") 

        if not has_consented and nonloop and not adminpage:
            came_from = base64.b16encode(request.path.encode())
            return redirect(f"/consent?from={came_from.decode()}")
        return get_response(request)
    return middleware
