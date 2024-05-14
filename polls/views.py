from urllib.parse import urlencode

from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json
from kenar_example import settings
from user_management.models import Post


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET'])
def entry_endpoint(request):

    context = {
        'return_url': request.query_params.get('return_url'),
        'app_slug': request.query_params.get('app_slug'),
    }
    post_token = request.GET.get('post_token', None)
    scopes = '+'.join([
        f'CHAT_READ_POST_CONVERSATIONS__{post_token}',
        f'CHAT_SEND_MESSAGE_POST_CONVERSATIONS__{post_token}',
        f'ADDON_USER_APPROVED__{post_token}',
        'USER_ADDON_CREATE',
        'USER_PHONE',
    ])
    params = {
        'response_type': 'code',
        'client_id': settings.DIVAR_APP_SLUG,
        'redirect_uri': settings.DIVAR_FALLBACK_REDIRECT_URL,
        'scope': scopes,
        'state': post_token,
    }
    Post.objects.get_or_create(token=post_token)
    return redirect(settings.DIVAL_OAUTH_REDIRECT_URL + f'?{urlencode(params)}'.replace('%2B', '+'))
    # return render(request, 'start_service.html', context)
    # return HttpResponse(request.query_params.items())
