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
      quantity = strip_tags(request.POST.get("quantity"))
      item = get_object_or_404(CartItem, id=item_id, cart_id__user_id=request.user, cart_id__status='pending')
      item.quantity = quantity
      item.subtotal = item.quantity * item.price
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