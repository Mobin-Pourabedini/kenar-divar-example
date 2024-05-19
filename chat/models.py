from django.db import models

from user_management.models import Post


class ChatSession(models.Model):
    id = models.AutoField(primary_key=True)
    access_token = models.CharField(max_length=255, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='chat_sessions')
    user_id = models.CharField(max_length=255)
    peer_id = models.CharField(max_length=255)
    supplier_id = models.CharField(max_length=255)
    demand_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id[:4]} - {self.peer_id[:4]} - {self.supplier_id[:4]} - {self.demand_id[:4]}"
