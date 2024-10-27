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

# models.py
class CartItem(models.Model):
  cart_id = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  subtotal = models.DecimalField(max_digits=10, decimal_places=2)

  # Add a method to return product name
  @property
  def product_name(self):
    return self.product_id.name

class Order(models.Model):  
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  total_price = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return f'Order by {self.user_id.username} - {self.created_at}'

class OrderItem(models.Model):
  order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  # Set to NULL if product is deleted
  quantity = models.IntegerField()
  subtotal = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return f'{self.product.name} x {self.quantity}'