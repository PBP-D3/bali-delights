from django.db import models
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL

# Create your models here.
class Cart(models.Model):
  STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
  ]

  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
  total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Cart of {self.user.username} - {self.status}'

class CartItem(models.Model):
  cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  subtotal = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return f'{self.quantity} of {self.product.name} in cart {self.cart.id}'