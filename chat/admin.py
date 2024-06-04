from django.contrib import admin

from chat.models import ChatSession


@admin.register(ChatSession)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'peer_id', 'supplier_id', 'demand_id', 'created_at', 'updated_at')
