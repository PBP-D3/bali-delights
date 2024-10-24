from django.urls import path
from carts.views import show_carts

app_name = 'carts'

urlpatterns = [
    path('', show_carts, name='show_carts'),
]

