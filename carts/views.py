from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.db import transaction
from .models import Cart, CartItem
from django.utils.html import strip_tags
from .forms import PasswordConfirmForm, CartItemUpdateForm
from decimal import Decimal
from products.models import Product


@login_required
def cart_view(request):
  # Get or create a pending cart for the user
  cart, created = Cart.objects.get_or_create(user_id=request.user, status='pending')
  
  # Select related items and calculate the total price
  items = cart.items.select_related('product_id')
  total_price = sum(item.subtotal for item in items)
  
  # Initialize the password confirmation form
  form = PasswordConfirmForm(user=request.user)
  
  context = {'cart': cart, 'items': items, 'total_price': total_price, 'form': form, 'user':request.user}
  
  return render(request, 'carts.html', context)

@csrf_exempt
@login_required
def update_cart_item(request):
  if request.method == "POST":
    form = CartItemUpdateForm(request.POST)
    if form.is_valid():
      item_id = strip_tags(request.POST.get("item_id"))
      quantity = int(strip_tags(request.POST.get("quantity")))  # Convert to int
      item = get_object_or_404(
        CartItem, 
        id=item_id, 
        cart_id__user_id=request.user, 
        cart_id__status='pending'
      )
      item.quantity = quantity
      item.subtotal = item.quantity * item.price  # This will now work correctly
      item.save()
      return JsonResponse({"success": True, "subtotal": item.subtotal})
  return JsonResponse({"success": False}, status=400)

@csrf_exempt
@login_required
@transaction.atomic
def submit_order(request):
  if request.method == "POST":
    form = PasswordConfirmForm(request.user, request.POST)
    if form.is_valid():
      cart = get_object_or_404(Cart, user_id=request.user, status='pending')
      items = cart.items.select_related('product_id')
      total_price = sum(item.subtotal for item in items)
      
      if request.user.money < total_price:
        return JsonResponse({"success": False, "message": "Insufficient funds."})
      
      # Update user balance and stock
      request.user.money -= total_price
      request.user.save()
      for item in items:
        item.product_id.stock -= item.quantity
        item.product_id.save()
      
      cart.status = 'paid'
      cart.total_price = total_price
      cart.save()
      return JsonResponse({"success": True, "total_price": total_price, "remaining_balance": request.user.money})
  return JsonResponse({"success": False}, status=400)

@login_required
def receipt_view(request, cart_id):
  cart = get_object_or_404(Cart, id=cart_id, user_id=request.user, status='paid')
  items = cart.items.select_related('product_id')
  return render(request, 'order_receipt.html', {'cart': cart, 'items': items})

@login_required
def order_history(request):
  carts = Cart.objects.filter(user_id=request.user, status='paid').order_by('-created_at')
  return render(request, 'order_history.html', {'carts': carts})

@login_required
def show_products(request):
    products = Product.objects.all()  # Retrieve all products from the database
    context = {
        'products': products
    }
    
    return render(request, "test_prod.html", context)

@csrf_exempt  # Since we're using DOMPurify for sanitization
@login_required
def add_to_cart(request):
  if request.method == 'POST':
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user_id=request.user)

    if product.stock <= 0:
      return JsonResponse({'success': False, 'message': 'Stock is empty.'})

    cart_item, created = CartItem.objects.get_or_create(cart_id=cart, product_id=product, quantity=1, price=product.price, subtotal=quantity * product.price)

    # Update the total price of the cart
    cart.total_price = sum(item.subtotal for item in cart.items.all())
    cart.save()

    return JsonResponse({
      'success': True,
      'message': 'Product successfully added to cart!',
      'total_price': cart.total_price,
      'remaining_stock': product.stock - cart_item.quantity
    })
    
@csrf_exempt
@login_required
def remove_cart_item(request):
  if request.method == "POST":
    item_id = strip_tags(request.POST.get("item_id"))
    try:
      item = get_object_or_404(CartItem, id=item_id, cart_id__user_id=request.user, cart_id__status='pending')
      item.delete()  # Remove the item from the cart

      # Check if the cart is empty after removal
      if not CartItem.objects.filter(cart_id__user_id=request.user, cart_id__status='pending').exists():
        return JsonResponse({"success": True, "empty": True})  # Indicate cart is empty
      return JsonResponse({"success": True, "empty": False})

    except CartItem.DoesNotExist:
      return JsonResponse({"success": False, "message": "Item not found."}, status=404)

  return JsonResponse({"success": False}, status=400)