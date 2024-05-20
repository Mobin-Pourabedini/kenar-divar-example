from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from misc.oauth.oauth import generate_oauth_url


def index(request):
    return HttpResponse("Hello, I'm up!")


@api_view(['GET'])
def start_app(request):

    post_token = request.GET.get('post_token', None)
    return_url = request.GET.get('return_url', None)
    scopes = '+'.join([
        f'CHAT_READ_POST_CONVERSATIONS__{post_token}',
        f'CHAT_SEND_MESSAGE_POST_CONVERSATIONS__{post_token}',
        f'ADDON_USER_APPROVED__{post_token}',
        'USER_PHONE',
    ])
    oath_permission_url = generate_oauth_url(post_token=post_token, scopes=scopes, state=f"{post_token}:{return_url}")
    return redirect(oath_permission_url)
