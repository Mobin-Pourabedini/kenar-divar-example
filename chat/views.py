import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from chat.models import ChatSession
from user_management.models import Post


@csrf_exempt
def start_chat_session(request):
    print("start_chat_session")
    data = json.loads(request.body)
    print(data)
    post_token = data["post_token"]
    user_id = data["user_id"]
    peer_id = data["peer_id"]
    supplier_id = data["Supplier"]["id"]
    demand_id = data["demand"]["id"]
    ChatSession.objects.create(
        post=Post.objects.get(token=post_token),
        user_id=user_id,
        peer_id=peer_id,
        supplier_id=supplier_id,
        demand_id=demand_id
    )
    print(data)
    return JsonResponse({
      "status": "200",
      "message": "success",
      "url": "https://google.com"
    })
