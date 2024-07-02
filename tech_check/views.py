import requests
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view

from kenar_example import settings
from misc.oauth import generate_oauth_url, get_access_token
from tech_check.models import Report, Technician, Post, User
from tech_check.utils import apply_report_in_divar


def index(request):
    return HttpResponse("Hello, I'm up!")


@api_view(['GET'])
def start_app(request):

    post_token = request.GET.get('post_token', None)
    return_url = request.GET.get('return_url', None)
    scopes = ' '.join([
        f'CHAT_SEND_MESSAGE_POST_CONVERSATIONS__{post_token}',
        f'ADDON_USER_APPROVED__{post_token}',
        'USER_PHONE',
    ])
    print(request.GET)
    Post.objects.get_or_create(token=post_token)
    oath_permission_url = generate_oauth_url(post_token=post_token, scopes=scopes, state=f"{post_token}:{return_url}")
    return redirect(oath_permission_url)


@api_view(['GET'])
def oauth_callback(request):
    data = request.query_params
    post_token_and_return_url = data.get('state')
    post_token, return_url = post_token_and_return_url.split(':', maxsplit=1)
    if not return_url:
        return_url = "https://www.google.com"
    post = Post.objects.get(token=post_token)
    if not post:
        return HttpResponse("Post not found")
    post.code = data.get('code')
    post.save()
    response = get_access_token(post.code)
    post.access_token = response.get('access_token')
    post.save()
    response = requests.post(settings.DIVAR_API_BASE_URL + '/v1/open-platform/users', headers={
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
    return render(request, 'submitted.html', {"return_url": return_url, "post_token": post_token})


@api_view(['POST'])
def patch_addon(request):
    data = request.POST
    post_token = data.get('post_token')
    battery_health = data.get('battery_health')
    camera_health = data.get('camera_health')
    body_health = data.get('physical_health')
    screen_health = data.get('screen_health')
    performance_health = data.get('performance')
    return_url = data.get('return_url')

    report = Report.objects.create(
        technician=Technician.objects.get_or_create(name='SELF REPORT', phone='0')[0],
        post=Post.objects.get(token=post_token),
        battery_health=int(battery_health),
        camera_health=int(camera_health),
        body_health=int(body_health),
        screen_health=int(screen_health),
        performance_health=int(performance_health),
    )
    response = apply_report_in_divar(report)
    if response.status_code != 200:
        return HttpResponse(response.json(), status=response.status_code)
    return redirect(return_url)
