from django.urls import path

from . import views

urlpatterns = [
    path("", views.start_chat_session, name="start_chat_session"),
]
