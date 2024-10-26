from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Store(models.Model):
  name = models.CharField(max_length=100)
  location = models.CharField(max_length=255, blank=True)
  description = models.TextField(blank=True)
  photo = models.CharField(max_length=255, blank=True)
  owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name