import requests

from kenar_example import settings


def send_message_in_session(session, message):
    response = requests.post(settings.DIVAR_OPEN_PLATFORM_BASE_URL + "/chat/conversation", headers={
        'content-type': 'application/json',
        'x-api-key': settings.DIVAR_API_KEY,
        'x-access-token': session.access_token,
    }, json={
        'post_token': session.post.token,
        'user_id': session.user_id,
        'peer_id': session.peer_id,
        'type': 'TEXT',
        'message': message
    })
    return response
