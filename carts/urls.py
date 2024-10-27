from django.urls import path
from . import views

app_name = "carts"

urlpatterns = [
  path('', views.cart_view, name='cart'),
  path('update-item/', views.update_cart_item, name='update_cart_item'),
  path('submit-order/', views.submit_order, name='submit_order'),
  path('<int:cart_id>/', views.receipt_view, name='receipt'),
  path('history/', views.order_history, name='order_history'),
]