from django.db import models
from django.contrib.auth.models import User
from stores.models import Store  # Assuming Store is in another app
from django.conf import settings

settings.AUTH_USER_MODEL

class Chat(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats_sent')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_chats')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.sender.username} and {self.store.name}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
