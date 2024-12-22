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

@csrf_exempt
@login_required
@require_POST
def add_product(request, store_id):
  if request.method == 'POST':
    # Sanitize input fields using escape or another clean method
    form_data = {field: escape(value) for field, value in request.POST.items()}
    form = ProductForm(form_data, request.FILES)
    
    if form.is_valid():
      product = form.save(commit=False)
      store = get_object_or_404(Store, id=store_id)
      product.store_id = store
      product.save()
      return JsonResponse({"success": True})
    
    else:
      return JsonResponse({
        "success": False,
        "message": "Form validation error.",
        "errors": form.errors
      })
  return JsonResponse({"success": False, "message": "Invalid request."})

def show_products(request, category=None):
   # Category filter
    if request.method == 'GET' and 'category' in request.GET:
        category = request.GET.get('category')
        
    search_query = strip_tags(request.GET.get('search', ''))

    products = Product.objects.all().annotate(average_rating=Avg('review__rating'))

    # Apply category filtering if provided
    if category:
        products = products.filter(category=category)
    
    if search_query:
        products = products.filter(name__icontains=search_query)

    sort_order = request.GET.get('sort', 'id')
    if sort_order == 'desc':
        products = products.order_by('-price')
    elif sort_order == 'asc':
        products = products.order_by('price')
    else:
        products = products.order_by('id')
        
    # Get unique categories for the filter dropdown
    categories = Product.CATEGORY_CHOICES

    # Prepare context for rendering the full HTML view
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'sort_order': sort_order,
        'search_query': request.GET.get('search', ''),
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
