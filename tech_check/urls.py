from django.urls import path

from . import views

urlpatterns = [
    path("start_app/", views.start_app, name="start_app"),
    path("is_up/", views.index, name="is_up"),
    path("oauth/callback/", views.oauth_callback, name="entry_endpoint"),
    path("patch_addon/", views.patch_addon, name="patch_addon")
]
