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
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()  

    # Sort products by price if specified in the query parameter
    sort_order = request.GET.get('sort', 'asc')  # Default sort is ascending
    if sort_order == 'desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('price')

    # Get unique categories for the filter dropdown
    categories = Product.CATEGORY_CHOICES

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
