import base64
import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from chat.models import ChatSession
from kenar_example import settings
from misc.oauth import generate_oauth_url, get_access_token
from misc.utils import send_message_in_session
from tech_check.models import Post


@csrf_exempt
def start_chat_session(request):
    data = json.loads(request.body)
    post_token = data["post_token"]
    user_id = data["user_id"]
    peer_id = data["peer_id"]
    supplier_id = data["supplier"]["id"]
    demand_id = data["demand"]["id"]
    return_url = data["callback_url"]
    chat_session, created = ChatSession.objects.get_or_create(
        post=Post.objects.get_or_create(token=post_token)[0],
        user_id=user_id,
        peer_id=peer_id,
        supplier_id=supplier_id,
        demand_id=demand_id
    )
    permission_url = generate_oauth_url(
        post_token=post_token,
        scopes=f"CHAT_SEND_MESSAGE_OAUTH__{base64_str(f'{user_id}:{post_token}:{peer_id}')}",
        state=f"{chat_session.id}:{return_url}",
        fallback_redirect_url=settings.APP_BASE_URL + '/chat/oauth/callback'
    )
    return JsonResponse({
      "status": "200",
      "message": "success",
      "url": permission_url
    })


def base64_str(base64_permission_details):
    b = base64.b64encode(base64_permission_details.encode('utf-8'))
    b64_permission_str = b.decode('utf-8')
    return b64_permission_str


@api_view(['GET'])
def chat_oauth_callback(request):
    data = request.query_params
    chat_session_id, return_url = data.get('state').split(":", maxsplit=1)
    chat_session = None

    try:
        chat_session = ChatSession.objects.get(id=chat_session_id)
    except Exception as e:
        return HttpResponse("Chat session not found")

    response = get_access_token(data.get('code'))

    if response.get("access_token") is None:
        return redirect(return_url)

    chat_session.access_token = response["access_token"]
    chat_session.refresh_token = response["refresh_token"]
    chat_session.access_token_expires_at = datetime.fromtimestamp(int(response["expires"]))
    chat_session.save()

    return render(request, 'chat_menu.html', context={
        'chat_session_id': chat_session_id,
        'return_url': return_url
    })


@api_view(['POST'])
def send_message(request):
    data = request.POST
    chat_session_id = data["chat_session_id"]
    return_url = data["return_url"]
    message = data["message"]
    chat_session = None

    try:
        chat_session = ChatSession.objects.get(id=chat_session_id)
    except Exception as e:
        return HttpResponse("Chat session not found")

    response = send_message_in_session(chat_session, message)
    if response.status_code != 200:
        return HttpResponse(response.json())
    return redirect(return_url)
