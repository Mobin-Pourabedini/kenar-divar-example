import logging
from urllib.parse import urlencode

import requests

from kenar_example import settings
from tech_check.models import Post

logger = logging.getLogger(__name__)

OAUTH_ENDPOINT = 'https://api.divar.ir/v1/open-platform/oauth/access_token'


def get_access_token(code):
    headers = {
        'x-api-key': settings.DIVAR_API_KEY,
        'content-type': 'application/json',
    }
    json_data = {
        "code": code,
        "client_id": settings.DIVAR_APP_SLUG,
        "client_secret": settings.DIVAR_API_KEY,
        "grant_type": "authorization_code",
    }

    res = requests.post(OAUTH_ENDPOINT, headers=headers, json=json_data)

    logger.info("message has been send to divar.")
    logger.info(res.json())
    logger.info(res.status_code)

    return res.json()


def generate_oauth_url(post_token, scopes, state, fallback_redirect_url=settings.DIVAR_FALLBACK_REDIRECT_URL):
    params = {
        'response_type': 'code',
        'client_id': settings.DIVAR_APP_SLUG,
        'redirect_uri': fallback_redirect_url,
        'scope': scopes,
        'state': state
    }
    Post.objects.get_or_create(token=post_token)
    oath_permission_url = settings.DIVAL_OAUTH_REDIRECT_URL + f'?{urlencode(params)}'
    return oath_permission_url
