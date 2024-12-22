from django.urls import path
from . import views

app_name = "carts"

urlpatterns = [
  path('', views.cart_view, name='cart'),
<<<<<<< HEAD
<<<<<<< HEAD
  path('<int:cart_id>/', views.receipt_view, name='receipt'),
=======
  path('receipt/<int:order_id>/', views.receipt_view, name='receipt_view'),  
>>>>>>> 5a9e59f7027c96c63041055472554c90239d653d
=======
  path('receipt/<int:order_id>/', views.receipt_view, name='receipt_view'),  
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
  path('history/', views.order_history, name='order_history'),
  path('api/submit-order/', views.submit_order, name='submit_order'),
  path('api/add-to-cart/', views.add_to_cart, name='add_to_cart'),
  path('api/update-item/', views.update_cart_item, name='update_cart_item'),
  path('api/remove-item/', views.remove_cart_item, name='remove_cart_item'),  
<<<<<<< HEAD
<<<<<<< HEAD
  path('products/', views.show_products, name='show_products'),
=======
>>>>>>> 5a9e59f7027c96c63041055472554c90239d653d
=======
  path('api/cart/', views.cart_view_json, name='cart_json'),
  path('api/history/', views.order_history_json, name='order_history_json'),
  path('api/receipt/<int:order_id>/', views.receipt_view_json, name='receipt_json'),
>>>>>>> f8b43257d2a50c14e7a6b1b8c4d61569b9cc8b77
]