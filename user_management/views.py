from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(['GET'])
def oauth_callback(request):
    return HttpResponse(request.query_params.items())
