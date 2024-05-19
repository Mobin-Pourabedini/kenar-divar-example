import logging
from urllib.parse import urlencode

import requests

from kenar_example import settings
from user_management.models import Post

logger = logging.getLogger(__name__)


class OAuthService:
    OAUTH_ENDPOINT = 'https://api.divar.ir/v1/open-platform/oauth/access_token'

    def __init__(self, client_secret, app_slug) -> None:
        self._client_secret = client_secret
        self._app_slug = app_slug

    def get_access_token(self, code):
        headers = {
            'x-api-key': self._client_secret,
            'content-type': 'application/json',
        }
        json_data = {
            "code": code,
            "client_id": self._app_slug,
            "client_secret": self._client_secret,
            "grant_type": "authorization_code",
        }

        res = requests.post(self.OAUTH_ENDPOINT, headers=headers, json=json_data)

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
    oath_permission_url = settings.DIVAL_OAUTH_REDIRECT_URL + f'?{urlencode(params)}'.replace('%2B', '+')
    return oath_permission_url
