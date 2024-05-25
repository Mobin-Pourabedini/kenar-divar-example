Kenar Divar Plugins

A Quick Start to develop a plugin

## Introduction

Divar is a popular classified ads platform in Iran. It provides a platform for users to post ads and chat with each other. Divar also provides a platform for developers to create plugins to extend the functionality of the platform.
Divar has provided a set of APIs for developers to create plugins. These APIs allow developers to interact with Divar,
such as patching addons to ads, sending messages in chats, and more.

In this document, we will guide you through the process of creating a simple plugin for Divar.

## Prerequisites
* A Divar account in the [developer panel](https://divar.ir/kenar)
* A basic understanding of the Divar platform
* A basic understanding of django

## Outline
### Starting app from post management panel
In The developer panel you provide the endpoints for your plugin, divar will send requests to the provided endpoint to start your
web application, you should either get some permissions by redirecting user to the oauth of divar or redirect user to the main page of your web application.
<br>
Divar will send a request to your endpoint with the following parameters:
<br>
```json
{ 
    "post_token": "<post_token>",
    "return_url": "<return_url>"
}
```
* `post_token` is the token of the ad from which the user got to your application.
* `return_url` is the url that the user should be redirected to after the process is done.

#### OAUTH
In order to get permissions from the user, you should redirect the user to the oauth of divar with the following parameters:

| Parameter Name | Value      | Description                                                                                                                                                                                                                                                           |
|----------------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| response_type  | 'code'     | The value returned after redirecting the user from the Divar open authentication page to your page, which you specify in the `redirect_uri` parameter.                                                                                                                |
| client_id      | <app-slug> | The unique name of your application that you can see in the application management section of the Divar panel.                                                                                                                                                        |
| redirect_uri   | <url>      | An address from your application to which the user is redirected after granting (or denying) the requested permissions. (This address must be URL encoded, listed in your application's allowed addresses in the Divar panel, and should not contain any parameters). |
| scope          | <scope>    | The permissions required to receive from the user, separated by a +.                                                                                                                                                                                                  |
| state          | <state>    | An arbitrary value that is included in the URL parameters when the user returns to your application.                                                                                                                                                                  |

- In this repo the function `get_oauth_url` is responsible for generating the url for the oauth.
```python
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
```

After the user grants the permissions, Divar will redirect the user to the `redirect_uri` with the following parameters:

| Parameter Name | Value   | Description                                                                                                                                |
|----------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------|
| code           | code    | If the user has agreed to your permission request, you will receive this value. Otherwise, you can show the appropriate error to the user. |
| state          | <state> | You receive the same value here that you placed in the `state` parameter in the previous section.                                          |

then you can exchange the code for an access token by sending a post request to the following endpoint:
```http request
POST https://api.divar.ir/v1/open-platform/oauth/access_token

{
  "code": "{{code}}",
  "client_id": "{{app_slug}}",
  "client_secret": "{{api_key}}",
  "grant_type": "authorization_code",
}
```
- in this repo the function `get_access_token` is responsible for exchanging the code for an access token.
```python
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
```
In response to this request, you will receive an `access_token`, a `refresh_token` and `expires`.
* `access_token` is the token that you should use to send requests to the Divar API.
* `refresh_token` is the token that you should use to get a new `access_token` when the `access_token` expires.
* `expires` is the time in seconds that the `access_token` is valid.

#### Patch an addon using the access token
following widgets are provided by divar to be used in the addons:
you can read more about the widgets [here](https://github.com/divar-ir/kenar-docs/blob/master/widgets/ReadMe.md)
```python
response = requests.post(settings.DIVAR_OPEN_PLATFORM_BASE_URL + f'/add-ons/post/{post.token}', headers={
    'content-type': 'application/json',
    'x-api-key': settings.DIVAR_API_KEY,
    'x-access-token': post.access_token,
}, json={
    'widgets': {
        'widget_list': [
            # legend_title function returns a widget definition for a legend title (in misc/widgets.py)
            legend_title(title="TechCheck Mobile", subtitle="کارشناسی گوشی موبایل", has_divider=True),
            
            # group_info function returns a widget definition for a group info (in misc/widgets.py)
            group_info({
                "سلامت باتری": f"{report.battery_health}%",
                "سلامت صفحه نمایش": f"{report.screen_health}%",
                "سلامت دوربین": f"{report.camera_health}%",

            }),
            
            # score_row function returns a widget definition for a score row (in misc/widgets.py)
            score_row(title="سلامت بدنه", percentage_score=report.body_health
                      , score_color="SUCCESS_PRIMARY", has_divider=True),
            score_row(title="سلامت پردازنده", percentage_score=report.performance_health
                      , score_color="SUCCESS_PRIMARY", has_divider=True),
            
            # evaluation_row function returns a widget definition for an evaluation row (in misc/widgets.py)
            evaluation_row(int(total_evaluation))
        ]
    },
    "semantic": {
        "year": "1398",
        "usage": "100000"
    },
    "notes": "any notes you want to get back on list api"
})
```
