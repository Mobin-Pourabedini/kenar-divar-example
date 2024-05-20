from django.contrib import admin

from chat.models import ChatSession, ChatMessage


@admin.register(ChatSession)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'peer_id', 'supplier_id', 'demand_id', 'created_at', 'updated_at')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'peer_id', 'message', 'created_at')
