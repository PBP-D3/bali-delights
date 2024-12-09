from django.urls import path
from chats.views import (
    list_chats,
    get_chat_messages,
    chat_with_store,
    send_message,
    get_stores,
    create_chat,
    delete_chat,
    edit_message,
    chat_with_cust,
    chats_view
)

urlpatterns = [
    # Main chat list page for normal users
    path('', list_chats, name='list_chats'),

    # Main chat interface view for both user types (normal user and shop owner)
    path('chats/', chats_view, name='chats_view'),

    # Chat-related API endpoints
    path('api/chats/<int:chat_id>/messages/', get_chat_messages, name='get_chat_messages'),
    path('api/chats/create/', create_chat, name='create_chat'),
    path('api/chats/<int:chat_id>/send/', send_message, name='send_message'),
    path('api/chats/<int:chat_id>/delete/', delete_chat, name='delete_chat'),

    # Specific chat views
    path('api/chats/store/<int:store_id>/', chat_with_store, name='chat_with_store'),
    path('api/chats/store/<int:store_id>/customer/<int:customer_id>/', chat_with_cust, name='chat_with_cust'),

    # Message-related API endpoints
    path('api/messages/<int:message_id>/edit/', edit_message, name='edit_message'),

    # Store-related API endpoints
    path('api/stores/', get_stores, name='get_stores'),
]
