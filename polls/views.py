from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET'])
def entry_endpoint(request):
    # Retrieve query parameters
    app_slug = request.GET.get('app_slug', '')
    post_token = request.GET.get('post_token', '')
    return_url = request.GET.get('return_url', '')
    #
    # # Process the query parameters and perform necessary actions
    data = {
        'app_slug': app_slug,
        'post_token': post_token,
        'return_url': return_url,
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
