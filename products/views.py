from django.shortcuts import render

# Create your views here.
# Create your views here.
def show_products(request):
    context = {
        'npm' : '2306220444',
        'name': request.user.username,
        'class': 'PBP D',
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "products.html", context)