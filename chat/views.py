import base64
import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from chat.models import ChatSession
from kenar_example import settings
from misc.oauth.oauth import generate_oauth_url, OAuthService
from misc.utils import send_message_in_session
from user_management.models import Post


@csrf_exempt
def start_chat_session(request):
    print("start_chat_session")
    data = json.loads(request.body)
    print(data)
    post_token = data["post_token"]
    user_id = data["user_id"]
    peer_id = data["peer_id"]
    supplier_id = data["supplier"]["id"]
    demand_id = data["demand"]["id"]
    ChatSession.objects.create(
        post=Post.objects.get_or_create(token=post_token)[0],
        user_id=user_id,
        peer_id=peer_id,
        supplier_id=supplier_id,
        demand_id=demand_id
    )
    base64_permission_details = f"{user_id}:{post_token}:{peer_id}"
    b = base64.b64encode(base64_permission_details.encode('utf-8'))
    b64_permission_str = b.decode('utf-8')
    scopes = '+'.join([
        f"CHAT_SEND_MESSAGE_OAUTH__{b}"
    ])
    chat_session = ChatSession.objects.create(
        post=Post.objects.get_or_create(token=post_token)[0],
        user_id=user_id,
        peer_id=peer_id,
        supplier_id=supplier_id,
        demand_id=demand_id
    )
    permission_url = generate_oauth_url(
        post_token, scopes,
        state=chat_session.id,
        fallback_redirect_url=settings.APP_BASE_URL + '/chat/oauth/fallback'
    )
    print(data)
    return JsonResponse({
      "status": "200",
      "message": "success",
      "url": permission_url
    })


@api_view(['GET'])
def chat_oauth_fallback(request):
    data = request.query_params
    chat_session_id = data.get('state')
    chat_session = None
    try:
        chat_session = ChatSession.objects.get(id=chat_session_id)
    except Exception as e:
        return HttpResponse("Chat session not found")
    oauth_service = OAuthService(client_secret=settings.DIVAR_API_KEY, app_slug=settings.DIVAR_APP_SLUG)
    access_token = oauth_service.get_access_token(data.get('code'))
    chat_session.access_token = access_token
    chat_session.save()
    context = {
        'chat_session_id': chat_session_id,
    }
    return render(request, 'chat_menu.html', context)


@api_view(['POST'])
def send_message(request):
    data = json.loads(request.body)
    chat_session_id = data["chat_session_id"]
    message = data["message"]
    chat_session = None

    try:
        chat_session = ChatSession.objects.get(id=chat_session_id)
    except Exception as e:
        return HttpResponse("Chat session not found")

    res = send_message_in_session(chat_session, message)
    return JsonResponse(res.json())
