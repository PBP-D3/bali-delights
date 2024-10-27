# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal  # Import Decimal here
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product

User = get_user_model()

class CartViewTests(TestCase):

  def setUp(self):
    # Create test users
    self.user = User.objects.create_user(username='testuser', password='testpassword')
    self.store_owner = User.objects.create_user(username='storeowner', password='storepassword')
    self.product = Product.objects.create(name='Test Product', price=Decimal('10.00'), stock=10, store_id=self.store_owner)
    self.client.login(username='testuser', password='testpassword')

  def test_cart_view(self):
    response = self.client.get(reverse('carts:cart'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'carts.html')

  def test_submit_order_success(self):
    # Create a cart and add an item to it
    cart = Cart.objects.create(user=self.user, status='pending')
    CartItem.objects.create(cart_id=cart, product_id=self.product, quantity=1, price=self.product.price, subtotal=self.product.price)

    # Update user money to allow for a successful order
    self.user.money = 50
    self.user.save()

    response = self.client.post(reverse('carts:submit_order'), {'password': 'testpassword'})
    self.assertEqual(response.status_code, 200)
    self.assertJSONEqual(str(response.content, encoding='utf-8'), {
      "success": True,
      "total_price": "10.00",
      "remaining_balance": "40.00"
    })
    self.assertEqual(Order.objects.count(), 1)
    self.assertEqual(OrderItem.objects.count(), 1)
    self.assertEqual(cart.status, 'paid')

  def test_submit_order_insufficient_funds(self):
    cart = Cart.objects.create(user=self.user, status='pending')
    CartItem.objects.create(cart_id=cart, product_id=self.product, quantity=1, price=self.product.price, subtotal=self.product.price)

    # Set user money to less than total price
    self.user.money = 5
    self.user.save()

    response = self.client.post(reverse('carts:submit_order'), {'password': 'testpassword'})
    self.assertJSONEqual(str(response.content, encoding='utf-8'), {
      "success": False,
      "message": "Insufficient funds."
    })

  def test_order_history_view(self):
    response = self.client.get(reverse('carts:order_history'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'order_history.html')

  def test_receipt_view(self):
    cart = Cart.objects.create(user=self.user, status='pending')
    cart_item = CartItem.objects.create(cart_id=cart, product_id=self.product, quantity=1, price=self.product.price, subtotal=self.product.price)

    # Update user money to allow for a successful order
    self.user.money = 50
    self.user.save()

    response = self.client.post(reverse('carts:submit_order'), {'password': 'testpassword'})
    order = Order.objects.first()

    response = self.client.get(reverse('carts:receipt_view', args=[order.id]))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'order_receipt.html')
    self.assertContains(response, self.product.name)

  def test_add_to_cart(self):
    response = self.client.post(reverse('carts:add_to_cart'), {
      'product_id': self.product.id,
      'quantity': 1
    })
    self.assertJSONEqual(str(response.content, encoding='utf-8'), {
      'success': True,
      'message': 'Product successfully added to cart!',
      'total_price': Decimal('10.00'),
      'remaining_stock': 9
    })

  def test_add_to_cart_insufficient_stock(self):
    self.product.stock = 0
    self.product.save()
    
    response = self.client.post(reverse('carts:add_to_cart'), {
      'product_id': self.product.id,
      'quantity': 1
    })
    self.assertJSONEqual(str(response.content, encoding='utf-8'), {
      'success': False,
      'message': 'Stock is empty.'
    })

  def test_remove_cart_item(self):
    cart = Cart.objects.create(user=self.user, status='pending')
    cart_item = CartItem.objects.create(cart_id=cart, product_id=self.product, quantity=1, price=self.product.price, subtotal=self.product.price)

    response = self.client.post(reverse('carts:remove_cart_item'), {
      'item_id': cart_item.id
    })
    self.assertJSONEqual(str(response.content, encoding='utf-8'), {
      'success': True,
      'empty': True
    })
    self.assertEqual(CartItem.objects.count(), 0)

  def test_update_cart_item(self):
    cart = Cart.objects.create(user=self.user, status='pending')
    cart_item = CartItem.objects.create(cart_id=cart, product_id=self.product, quantity=1, price=self.product.price, subtotal=self.product.price)

    response = self.client.post(reverse('carts:update_cart_item'), {
      'item_id': cart_item.id,
      'quantity': 2
    })
    self.assertJSONEqual(str(response.content, encoding='utf-8'), {
      'success': True,
      'subtotal': '20.00'
    })
    cart_item.refresh_from_db()
    self.assertEqual(cart_item.quantity, 2)