from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entry_endpoint/", views.entry_endpoint, name="entry_endpoint"),
]
