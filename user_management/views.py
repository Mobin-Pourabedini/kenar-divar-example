import requests
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from kenar_example import settings
from user_management.models import Post


@api_view(['GET'])
def oauth_callback(request):
    data = request.query_params
    post_token = data.get('state')
    post = Post.objects.get(token=post_token)
    if not post:
        return HttpResponse(status=400)
    post.code = data.get('code')
    post.save()
    response = requests.post(settings.DIVAR_OAUTH_ACCESS_TOKEN_URL, headers={
        'x-api-key': settings.DIVAR_API_KEY,
        'content-type': 'application/json',
    }, json={
        'code': post.code,
        'client_id': settings.DIVAR_APP_SLUG,
        'client_secret': settings.DIVAR_API_KEY,
        'grant_type': 'authorization_code',
    })
    print(response.json())
    post.access_token = response.json().get('access_token')
    post.save()
    return HttpResponse("Success")
