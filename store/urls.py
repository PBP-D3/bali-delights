from django.urls import path
from store.views import show_store

app_name = 'store'

urlpatterns = [
    path('', show_store, name='show_store'),
]

