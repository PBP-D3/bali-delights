from django.urls import path
from chats.views import list_chats, get_chat_messages, chat_with_store, send_message, add_chat, get_stores, create_chat

urlpatterns = [
    # Main chat list page
    path('', list_chats, name='list_chats'),

    # Page to add a new chat
    path('add/', add_chat, name='add_chat'),

    # Specific chat view with store
    path('<int:store_id>/', chat_with_store, name='chat_with_store'),

    # AJAX endpoint to fetch messages for a specific chat
    path('api/chats/<int:chat_id>/messages/', get_chat_messages, name='get_chat_messages'),

    # API endpoint to create a new chat with a store
    path('api/chats/create/', create_chat, name='create_chat'),  # Rename for clarity

    # API endpoint to send a message within an existing chat
    path('api/chats/<int:chat_id>/send/', send_message, name='send_message'),  # For actual messaging in chat

    # API endpoint to get the list of stores
    path('api/stores/', get_stores, name='get_stores'),
]
