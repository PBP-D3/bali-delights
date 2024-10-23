from django.urls import path
from products.views import show_products

app_name = 'products'

urlpatterns = [
    path('', show_products, name='show_products'),
]

