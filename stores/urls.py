from django.urls import path
from stores.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'stores'

urlpatterns = [
    path('', show_stores, name='show_stores'),
    path('register/', register_store, name='register_store'),
    path('<int:id>/', show_store_details, name='show_store_details'),
    path('load-all-stores/', load_all_stores, name='load_all_stores'),
    path('my-store/', show_user_store, name='show_user_store'),
    path('register-store/', register_store, name='register_store'),
    path('register-store-flutter/', register_store_flutter, name='register_store_flutter'),
    path('edit/<int:id>/', edit_store, name='edit_store'),
    path('delete/<int:id>/', delete_store, name='delete_store'),
    path('owner/<int:id>/', owner_store_view, name='owner_store_view'),
    path('search/', search_stores, name='search_stores'),
    path('json/', show_json, name='show_json'),
    path('owner_json/', show_json_by_owner, name='show_json_by_owner'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('edit-flutter/<int:store_id>/', edit_store_flutter, name='edit_store_flutter'),
    path('delete-flutter/<int:store_id>/', delete_store_flutter, name='delete_store_flutter'),
]
