from django.core.management.base import BaseCommand

from chat.models import ChatSession
from chat.views import register_webhook
from misc.utils import send_message_in_session


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        session = ChatSession.objects.filter(id=148).first()
        resp = register_webhook(session)
        print(resp.json())
