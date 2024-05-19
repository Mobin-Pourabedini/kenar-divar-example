from django.core.management.base import BaseCommand

from chat.models import ChatSession
from misc.utils import send_message_in_session


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        session = ChatSession.objects.filter(post__token="gZEhY4g7").first()
        response = send_message_in_session(session, 'سلام بر تو :)')
        print(response.json())
        print(session)
