import logging
import requests

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
