from django.urls import path

from . import views

urlpatterns = [
    path("callback/", views.oauth_callback, name="entry_endpoint"),
    path("debug/", views.debug, name="debug"),
    path("patch_addon/", views.patch_addon, name="patch_addon")
]
