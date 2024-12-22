from django.db import models
from stores.models import Store

# Create your models here.
class Product(models.Model):
  CATEGORY_CHOICES = [
    ('Clothes', 'Clothes'),
    ('Jewelries', 'Jewelries'),
    ('Crafts', 'Crafts'),
    ('Arts', 'Arts'),
    ('Snacks', 'Snacks'),
    ('Drinks', 'Drinks'),
  ]

  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.PositiveIntegerField()
  category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
  store_id = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  photo_upload = models.ImageField(upload_to='product_images/', blank=True, null=True)
  photo_url = models.URLField(blank=True, null=True)
  
  def get_image(self):
      if self.photo_url:
          return self.photo_url
      elif self.photo_upload:
          return self.photo_upload.url
      return "https://img.freepik.com/premium-vector/shop-vector-design-white-background_917213-257003.jpg?semt=ais_hybrid"

  def __str__(self):
    return self.name