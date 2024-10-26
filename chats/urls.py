from django.urls import path
from chats.views import list_chats, get_chat_messages, chat_with_store, send_message

urlpatterns = [
    # List all chats for the user
    path('', list_chats, name='list_chats'),  # Now accessible at '/chats/'

    # View a specific chat with a store (initial page load for chat)
    path('<int:store_id>/', chat_with_store, name='chat_with_store'),  # Now accessible at '/chat/<store_id>/'

    # API to fetch chat messages for real-time updates (AJAX)
    path('api/<int:chat_id>/messages/', get_chat_messages, name='get_chat_messages'),  # Now accessible at '/chat/api/<chat_id>/messages/'

    # API to send a message in a specific chat (AJAX)
    path('api/<int:chat_id>/send/', send_message, name='send_message'),  # Now accessible at '/chat/api/<chat_id>/send/'
]