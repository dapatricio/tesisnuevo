import time
from django.conf import settings
from django.contrib.auth import logout


class SessionIdleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if 'last_request' in request.session:
                elapsed = time.time() - request.session['last_request']
                if elapsed > settings.SESSION_COOKIE_AGE:
                    del request.session['last_request']
                    logout(request)
                    # flushing the complete session is an option as well!
                    # request.session.flush()
            request.session['last_request'] = time.time()
        else:
            if 'last_request' in request.session:
                del request.session['last_request']
        response = self.get_response(request)
        return response
