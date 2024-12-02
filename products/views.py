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
from django.core.paginator import Paginator

@login_required
@require_POST
def add_product(request):
    if request.method == "POST" and request.is_ajax():
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "message": "Form validation error."})
    return JsonResponse({"success": False, "message": "Invalid request."})

def show_products(request, category=None):
    # Category filter
    if request.method == 'GET' and 'category' in request.GET:
        category = request.GET.get('category')

    search_query = request.GET.get('search', '')
    
    products = Product.objects.all().annotate(average_rating=Avg('review__rating'))

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

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'sort_order': sort_order,
        'search_query': search_query,  
    }

    return render(request, "products.html", context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_detail.html", {"product": product})

def edit_product(request, product_id):
    product = Product.objects.get(pk = product_id)

    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('products:show_products'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    product.delete()

    return HttpResponseRedirect(reverse('products:show_products'))

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
    page_number = request.GET.get('page', 1)

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

    # Pagination
    paginator = Paginator(products, 10)  # 10 products per page
    page = paginator.get_page(page_number)

    # Serialize the products
    products_list = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category": product.get_category_display(),  # Human-readable category
            "image_url": product.image_url.url if product.image_url else None,
            "average_rating": product.average_rating,
        }
        for product in page
    ]

    # Response with pagination metadata
    response_data = {
        "products": products_list,
        "total_pages": paginator.num_pages,
        "current_page": page.number,
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
    }

    return JsonResponse(response_data, safe=False)