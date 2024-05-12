from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET'])
def entry_endpoint(request):
    context = {
        'return_url': request.query_params.get('return_url'),
        'app_slug': request.query_params.get('app_slug'),
    }
    return render(request, 'start_service.html', context)
    # return HttpResponse(request.query_params.items())
