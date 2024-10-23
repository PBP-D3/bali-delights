from django.urls import path
from chats.views import show_chats

app_name = 'chats'

urlpatterns = [
    path('', show_chats, name='show_chats'),
]