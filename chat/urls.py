from django.urls import path

from . import views

urlpatterns = [
    path("", views.start_chat_session, name="start_chat_session"),
    path("oauth/fallback", views.chat_oauth_fallback, name="chat_oauth_fallback"),
    path("send_message", views.send_message, name="send_message"),
]
