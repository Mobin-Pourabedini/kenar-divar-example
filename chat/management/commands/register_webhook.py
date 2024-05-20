from django.core.management.base import BaseCommand

from chat.models import ChatSession
from chat.views import register_webhook
from misc.utils import send_message_in_session


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        session = ChatSession.objects.filter(post__token="gZEhY4g7").first()
        register_webhook(session)
