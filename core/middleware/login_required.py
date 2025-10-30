from typing import Iterable
from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        login_url = getattr(settings, 'LOGIN_URL', '/admin/login/')
        exempt = [login_url, '/admin/login/', '/admin/password_reset/', '/api/token/', '/api/token/refresh/', '/favicon.ico', '/robots.txt']
        static_url = getattr(settings, 'STATIC_URL', 'static/') or ''
        media_url = getattr(settings, 'MEDIA_URL', 'media/') or ''
        if static_url:
            exempt.extend([static_url, '/' + static_url.lstrip('/')])
        if media_url:
            exempt.extend([media_url, '/' + media_url.lstrip('/')])

        extra = getattr(settings, 'LOGIN_EXEMPT_URLS', [])
        if isinstance(extra, Iterable):
            exempt.extend(list(extra))

        self.exempt_prefixes = [p if p.startswith('/') else '/' + p for p in exempt]

    def __call__(self, request):
        path = request.path_info

        if request.user.is_authenticated:
            return self.get_response(request)

        for pref in self.exempt_prefixes:
            if path.startswith(pref):
                return self.get_response(request)

        login_url = getattr(settings, 'LOGIN_URL', '/admin/login/')
       
        return redirect(f"{login_url}?next={request.path}")
