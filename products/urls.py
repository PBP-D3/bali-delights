from django.urls import path
from products.views import show_products, show_json, show_xml, show_json_by_id, show_xml_by_id,product_detail, edit_product, delete_product, add_product, api_get_products, api_get_products_by_store

app_name = 'products'

urlpatterns = [
    path('', show_products, name='show_products'),
    path('<int:product_id>/', product_detail, name='product_detail'),
    path('<str:category>/', show_products, name='show_products_by_category'),
    path('json/', show_json, name='show_json'),
    path('xml/', show_xml, name='show_xml'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('api/products/', api_get_products, name='api_get_products'), 
    path('api/store/<int:store_id>/add-product/', add_product, name='add_product'), 
    path('api/stores/<int:store_id>/products/', api_get_products_by_store, name='api_get_products_by_store'),  
    path('api/products/<int:product_id>/edit/', edit_product, name='edit_product'),  
    path('api/products/<int:product_id>/delete/', delete_product, name='delete_product'), 
]

