from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Store(models.Model):
  name = models.CharField(max_length=100)
  location = models.CharField(max_length=255, blank=True)
  description = models.TextField(blank=True)
  location = models.CharField(max_length=100)
  owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  photo_upload = models.ImageField(upload_to='store_images/', blank=True, null=True)  # for file uploads
  photo = models.URLField(blank=True, null=True)  # for URLs

  def get_image(self):
      """
      Returns the image URL or the uploaded image path if the URL isn't provided.
      """
      if self.photo:
          return self.photo
      elif self.photo_upload:
          return self.photo_upload.url
      return "https://img.freepik.com/premium-vector/shop-vector-design-white-background_917213-257003.jpg?semt=ais_hybrid"

  def __str__(self):
    return self.name