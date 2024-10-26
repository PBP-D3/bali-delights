from django.db import models
from django.conf import settings
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

User = settings.AUTH_USER_MODEL

# Create your models here.
class Review(models.Model):
  comment = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  rating = models.PositiveIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)],
    help_text="Rating should be between 1 and 5"
  )


  def __str__(self):
    return f'Review by {self.user.username} on {self.product.name}'

class Like(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Like by {self.user.username}'