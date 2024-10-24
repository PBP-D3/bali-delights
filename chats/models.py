from django.db import models
from django.conf import settings
from stores.models import Store

User = settings.AUTH_USER_MODEL

# Create your models here.
class Chat(models.Model):
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  store_id = models.ForeignKey(Store, on_delete=models.CASCADE)

  def __str__(self):
    return f'Message by {self.user.username} in store {self.store.name}'

class ChatMessage(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_messages')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message by {self.sender.username} in chat {self.chat.id}'