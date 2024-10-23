from django.urls import path
from product.views import show_product

app_name = 'product'

urlpatterns = [
    path('', show_product, name='show_product'),
]

