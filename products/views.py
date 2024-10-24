from django.shortcuts import render
from .models import Product

# Create your views here.
# Create your views here.
def show_products(request):
    products = Product.objects.all()  # Retrieve all products from the database
    context = {
        'name': request.user.username,
        'last_login': request.COOKIES['last_login'],
        'products': products
    }
    
    return render(request, "products.html", context)