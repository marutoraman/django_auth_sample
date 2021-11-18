from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

from app.settings import LOGOUT_URL


def logout_auth0(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri(LOGOUT_URL)})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)