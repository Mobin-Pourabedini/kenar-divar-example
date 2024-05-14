import requests
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from kenar_example import settings
from user_management.models import Post, User


@api_view(['GET'])
def oauth_callback(request):
    data = request.query_params
    post_token = data.get('state')
    post = Post.objects.get(token=post_token)
    if not post:
        return HttpResponse("Post not found")
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
    print("hell", response.json())
    post.access_token = response.json().get('access_token')
    post.save()
    response = requests.post(settings.DIVAR_OPEN_PLATFORM_BASE_URL + '/users', headers={
        'content-type': 'application/json',
        'x-api-key': settings.DIVAR_API_KEY,
        'x-access-token': post.access_token,
    })
    user, _ = User.objects.get_or_create(phone=response.json().get('phone_numbers')[0])
    if not user.access_token:
        user.access_token = post.access_token
        user.save()
    post.user = user
    post.save()
    return HttpResponse("Success")


@api_view(['GET'])
def debug(request):
    return render(request, 'after_auth.html')


# @api_view(['POST'])
# def create_addon(request):
    # data = request.data
    # post = Post.objects.get(token=data.get('post_token'))
    # if not post:
    #     return HttpResponse(status=400, reason='Post not found')
    # response = requests.post(settings.DIVAR_OPEN_PLATFORM_BASE_URL + f'/add-ons/post/{post.token}', headers={
    #     'content-type': 'application/json',
    #     'x-api-key': settings.DIVAR_API_KEY,
    #     'x-access-token': post.access_token,
    # }, json={
    #     'widgets': {
    #         'widget_list': [
    #             {
    #                 "widget_type": "LEGEND_TITLE_ROW",
    #                 "data": {
    #                     "@type": "type.googleapis.com/widgets.LegendTitleRowData",
    #                     "title": "hello addon",
    #                     "subtitle": "addon subtitle",
    #                     "has_divider": True,
    #                     "image_url": "logo"
    #                 }
    #             }
    #         ]
    #     },
    #     "semantic": {
    #         "year": 1398,
    #         "usage": 100000
    #     },
    #     "notes": "any notes you want to get back on list api"
    # })
    # if response.status_code != 200:
    #     return HttpResponse(status=400, reason='Failed to create addon')
    # return HttpResponse(status=200, reason='Addon created')
