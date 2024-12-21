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