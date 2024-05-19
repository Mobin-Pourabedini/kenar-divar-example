from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from misc.oauth.oauth import generate_oauth_url


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET'])
def entry_endpoint(request):

    context = {
        'return_url': request.query_params.get('return_url'),
        'app_slug': request.query_params.get('app_slug'),
    }
    post_token = request.GET.get('post_token', None)
    scopes = '+'.join([
        f'CHAT_READ_POST_CONVERSATIONS__{post_token}',
        f'CHAT_SEND_MESSAGE_POST_CONVERSATIONS__{post_token}',
        f'ADDON_USER_APPROVED__{post_token}',
        'USER_ADDON_CREATE',
        'USER_PHONE',
    ])
    oath_permission_url = generate_oauth_url(post_token=post_token, scopes=scopes, state=post_token)
    return redirect(oath_permission_url)
    # return render(request, 'start_service.html', context)
    # return HttpResponse(request.query_params.items())


