from django.urls import path

from . import views

urlpatterns = [
    path("start_app/", views.start_app, name="start_app"),
    path("is_up/", views.index, name="is_up"),
]
