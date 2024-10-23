from django.urls import path
from chat.views import show_chat

app_name = 'chat'

urlpatterns = [
    path('', show_chat, name='show_chat'),
]