from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from products.models import Product
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from products.forms import ProductForm
from django.http import JsonResponse
from django.db.models import Avg
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import ProductForm  # Ensure you import your ProductForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Product, Store
from django.utils.html import escape
from django.utils.html import strip_tags

@login_required
@require_POST
def add_product(request):
    print("test add")
    if request.user.role != "shop_owner":
        return JsonResponse({"success": False, "message": "Permission denied."})

    if request.method == "POST":
        print(request.POST)
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        category = request.POST.get("category")
        image_url = request.POST.get("image_url")
        user = request.user  

        new_product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image_url=image_url,
            store_id=user.store 
        )
        new_product.save()

        return JsonResponse({"success": True, "message": "Product added successfully!"})

    return JsonResponse({"success": False, "message": "Invalid request method."})

def show_products(request, category=None):
   # Category filter
    if request.method == 'GET' and 'category' in request.GET:
        category = request.GET.get('category')

    if category:
        products = products.filter(category=category)
    
    if search_query:
        products = products.filter(name__icontains=search_query)

    sort_order = request.GET.get('sort', 'id')
    if sort_order == 'desc':
        products = products.order_by('-price')
    elif sort_order == 'asc':
        products = products.order_by('price')

    # Get unique categories for the filter dropdown
    categories = Product.CATEGORY_CHOICES

    # Prepare context for rendering the full HTML view
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'sort_order': sort_order,
    }

    return render(request, "products.html", context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_detail.html", {"product": product})

def edit_product(request, product_id):
  product = get_object_or_404(Product, pk=product_id)
  
  form = ProductForm(request.POST or None, request.FILES or None, instance=product)

  if request.method == "POST":
    if form.is_valid():
        form.save()
        return redirect(reverse('stores:owner_store_view', args=[product.store_id.id]))
    else:
        print("Form errors:", form.errors)

  context = {'form': form, 'product': product}
  return render(request, "edit_product.html", context)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    product.delete()

    return HttpResponseRedirect(reverse('stores:owner_store_view', args=[product.store_id.id]))

def show_xml(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required
def api_get_products(request):
    # Optional filtering (search, category, etc.)
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', None)
    sort_order = request.GET.get('sort', 'id')

    products = Product.objects.all().annotate(average_rating=Avg('review__rating'))

    if category:
        products = products.filter(category=category)
    
    if search_query:
        products = products.filter(name__icontains=search_query)

    if sort_order == 'desc':
        products = products.order_by('-price')
    elif sort_order == 'asc':
        products = products.order_by('price')
    else:
        products = products.order_by('id')

    # Serialize the products
    products_list = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category": product.get_category_display(),  # Human-readable category
            "image_url": product.photo_upload.url if product.photo_upload else None,  
            "average_rating": product.average_rating,
        }
        for product in products
    ]

    # Return all products without pagination
    return JsonResponse({"products": products_list}, safe=False)