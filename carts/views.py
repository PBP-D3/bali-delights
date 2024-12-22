from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
<<<<<<< HEAD
<<<<<<< HEAD

from django.http import JsonResponse
from django.db import transaction
from .models import Cart, CartItem
from django.utils.html import strip_tags
from .forms import PasswordConfirmForm, CartItemUpdateForm
from decimal import Decimal
from products.models import Product


@login_required
def cart_view(request):
  # Ensure only one pending cart exists
  cart, created = Cart.objects.get_or_create(user_id=request.user, status='pending')

  # Select related items and calculate the total price
  items = cart.items.select_related('product_id')
  total_price = sum(item.subtotal for item in items)

  # Initialize the password confirmation form
  form = PasswordConfirmForm(user=request.user)

  context = {'cart': cart, 'items': items, 'total_price': total_price, 'form': form, 'user': request.user}

  return render(request, 'carts.html', context)

@csrf_exempt
@login_required
@transaction.atomic
def submit_order(request):
  if request.method == "POST":
    form = PasswordConfirmForm(request.user, request.POST)
    if form.is_valid():
      try:
        # Fetch the pending cart explicitly to avoid MultipleObjectsReturned error
        cart = Cart.objects.get(user_id=request.user, status='pending')
        
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

        # Clear cart items after purchase
        cart.items.all().delete()  # Clear cart items
        return JsonResponse({"success": True, "total_price": total_price, "remaining_balance": request.user.money})

      except Cart.DoesNotExist:
        return JsonResponse({"success": False, "message": "Cart not found."}, status=404)
      except Cart.MultipleObjectsReturned:
        return JsonResponse({"success": False, "message": "Multiple carts found. Please contact support."}, status=400)

  return JsonResponse({"success": False}, status=400)

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
=======
=======
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
from django.http import JsonResponse
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from .forms import PasswordConfirmForm
from products.models import Product
from decimal import Decimal
from django.utils.html import strip_tags

@login_required
def cart_view(request):
  cart, created = Cart.objects.get_or_create(user_id=request.user, status='pending')
  items = cart.items.select_related('product_id')
  total_price = sum(item.subtotal for item in items)
  
  form = PasswordConfirmForm(user=request.user)
  
  context = {
    'cart': cart,
    'items': items,
    'total_price': total_price,
    'form': form,
    'user': request.user
  }
  
  return render(request, 'carts.html', context)

@csrf_exempt
@login_required
@transaction.atomic
def submit_order(request):
  if request.method == "POST":
    form = PasswordConfirmForm(request.user, request.POST)
    if form.is_valid():
      try:
        # Fetch the user's pending cart
        cart = get_object_or_404(Cart, user_id=request.user, status='pending')
        items = cart.items.select_related('product_id')  # Use select_related for efficiency
        total_price = sum(item.subtotal for item in items)

        # Check for sufficient funds
        if request.user.money < total_price:
          return JsonResponse({"success": False, "message": "Insufficient funds."}, status=403)

        # Check if the user is trying to buy their own product
        for item in items:
          product = item.product_id
          if item.quantity > product.stock:
            return JsonResponse({
              "success": False,
              "message": f"Insufficient stock for {product.name}. Available stock: {product.stock}."
          }, status=403)
          if product.store_id.owner_id == request.user:
            return JsonResponse({"success": False, "message": "You cannot buy your own product."}, status=403)

        # Deduct from user's balance
        request.user.money -= total_price
        request.user.save()

        # Create the Order without storing cart_id since it will be emptied
        order = Order.objects.create(
          user_id=request.user,
          total_price=float(total_price)  # Ensure total_price is a float
        )

        # Now add items to the Order using the OrderItem model
        for item in items:
          OrderItem.objects.create(
            order=order,
            product=item.product_id,
            quantity=item.quantity,
            subtotal=float(item.subtotal)  # Convert to float for JSON serialization
          )
          # Pay the shop owner for the product sold
          product.store_id.owner_id.money += float(item.subtotal)  # Convert to float
          product.store_id.owner_id.save()

        # Clear cart items and update cart status
        cart.items.all().delete()  # Clear the cart items
        cart.status = 'paid'  # Update the cart status
        cart.save()

        return JsonResponse({
          "success": True,
          "total_price": total_price,
          "remaining_balance": request.user.money
        }, status=200)

      except Cart.DoesNotExist:
        return JsonResponse({"success": False, "message": "Cart not found."}, status=404)

  return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

@login_required
def order_history(request):
  orders = Order.objects.filter(user_id=request.user).order_by('-created_at')
  return render(request, 'order_history.html', {'orders': orders})

@login_required
def receipt_view(request, order_id):
  order = get_object_or_404(Order, id=order_id)

  # Retrieve associated order items
  items = order.order_items.all()  # Use related_name defined in OrderItem

  context = {
    'order': order,
    'items': items,
  }

  return render(request, 'order_receipt.html', context)

@csrf_exempt
@login_required
def remove_cart_item(request):
  if request.method == "POST":
    item_id = request.POST.get("item_id")
    try:
      item = get_object_or_404(CartItem, id=item_id, cart_id__user_id=request.user, cart_id__status='pending')
      item.delete()  # Remove the item from the cart

      # Check if the cart is empty after removal
      if not CartItem.objects.filter(cart_id__user_id=request.user, cart_id__status='pending').exists():
        return JsonResponse({"success": True, "empty": True})  # Indicate cart is empty
      return JsonResponse({"success": True, "empty": False})

    except CartItem.DoesNotExist:
      return JsonResponse({"success": False, "message": "Item not found."}, status=404)

@login_required
def show_products(request):
  products = Product.objects.all()  # Retrieve all products from the database
  context = {
    'products': products
  }
  return render(request, "test_prod.html", context)

@csrf_exempt
<<<<<<< HEAD
>>>>>>> 5a9e59f7027c96c63041055472554c90239d653d
=======
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
@login_required
def add_to_cart(request):
  if request.method == 'POST':
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)
<<<<<<< HEAD
<<<<<<< HEAD
    cart, created = Cart.objects.get_or_create(user_id=request.user)
=======
=======
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
    cart, created = Cart.objects.get_or_create(user_id=request.user, status='pending')

    # Check if user is trying to add their own product
    if product.store_id.owner_id == request.user:
      return JsonResponse({'success': False, 'message': 'You cannot add your own product to the cart.'}, status=403)
<<<<<<< HEAD
>>>>>>> 5a9e59f7027c96c63041055472554c90239d653d
=======
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77

    if product.stock <= 0:
      return JsonResponse({'success': False, 'message': 'Stock is empty.'})

<<<<<<< HEAD
<<<<<<< HEAD
    cart_item, created = CartItem.objects.get_or_create(cart_id=cart, product_id=product, quantity=1, price=product.price, subtotal=quantity * product.price)

    # Update the total price of the cart
=======
=======
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
    cart_item, created = CartItem.objects.get_or_create(
      cart_id=cart, 
      product_id=product, 
      defaults={'quantity': quantity, 'price': product.price, 'subtotal': quantity * product.price}
    )

    # Update total price of the cart
<<<<<<< HEAD
>>>>>>> 5a9e59f7027c96c63041055472554c90239d653d
=======
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
    cart.total_price = sum(item.subtotal for item in cart.items.all())
    cart.save()

    return JsonResponse({
      'success': True,
      'message': 'Product successfully added to cart!',
      'total_price': cart.total_price,
      'remaining_stock': product.stock - cart_item.quantity
    })
<<<<<<< HEAD
<<<<<<< HEAD
  
=======
    
  return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

>>>>>>> 5a9e59f7027c96c63041055472554c90239d653d
=======
    
  return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
@csrf_exempt
@login_required
def update_cart_item(request):
  if request.method == "POST":
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
    item_id = request.POST.get("item_id")
    quantity = int(request.POST.get("quantity"))  # Convert to int
    item = get_object_or_404(
      CartItem, 
      id=item_id, 
      cart_id__user_id=request.user, 
      cart_id__status='pending'
    )
    
    item.quantity = quantity
    # Check if quantity exceeds stock
    product = item.product_id
    if item.quantity > product.stock:
      return JsonResponse({
        "success": False,
        "message": f"Insufficient stock for {product.name}. Available stock: {product.stock}."
    })
    if item.quantity <= 0:
       return JsonResponse({
        "success": False,
        "message": f"Can't complete purchase with zero items!"
    })
    item.subtotal = item.quantity * item.price
    item.save()

    return JsonResponse({"success": True, "subtotal": item.subtotal})
  
  return JsonResponse({"success": False}, status=400)
<<<<<<< HEAD
>>>>>>> 5a9e59f7027c96c63041055472554c90239d653d
=======

@login_required
@csrf_exempt
def cart_view_json(request):
    cart, created = Cart.objects.get_or_create(user_id=request.user, status='pending')
    items = cart.items.select_related('product_id')
    total_price = sum(item.subtotal for item in items)
    
    items_data = [{
        'id': item.id,
        'product_name': item.product_id.name,
        'quantity': item.quantity,
        'price': float(item.price),
        'subtotal': float(item.subtotal),
        'image': item.get_image()
    } for item in items]
    
    return JsonResponse({
        'success': True,
        'cart': {
            'id': cart.id,
            'total_price': float(total_price),
            'items': items_data,
            'user': request.user.username
        }
    })

@login_required
@csrf_exempt
def order_history_json(request):
    sort_by = request.GET.get('sort_by', 'created_at')
    sort_direction = request.GET.get('sort_direction', 'asc')
    
    if sort_by not in ['created_at', 'total_price']:
        sort_by = 'created_at'
    
    if sort_direction == 'desc':
        orders = Order.objects.filter(user_id=request.user).order_by(f'-{sort_by}')
    else:
        orders = Order.objects.filter(user_id=request.user).order_by(sort_by)
    
    orders_data = [{
        'id': order.id,
        'total_price': float(order.total_price),
        'created_at': order.created_at.isoformat(),
        'items': [{
            'product': item.product.name if item.product else 'Deleted Product',
            'quantity': item.quantity,
            'subtotal': float(item.subtotal),
            'image': item.get_image()
        } for item in order.order_items.all()]
    } for order in orders]
    
    return JsonResponse({
        'success': True,
        'orders': orders_data
    })

@login_required
@csrf_exempt
def receipt_view_json(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.order_items.all()
    
    items_data = [{
        'product': item.product.name if item.product else 'Deleted Product',
        'quantity': item.quantity,
        'subtotal': float(item.subtotal),
        'image': item.get_image()
    } for item in items]
    
    return JsonResponse({
        'success': True,
        'order': {
            'id': order.id,
            'total_price': float(order.total_price),
            'created_at': order.created_at.isoformat(),
            'items': items_data
        }
    })
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
