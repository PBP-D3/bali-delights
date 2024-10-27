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
    chats_view  # Import the chats_view function
)

urlpatterns = [
    # Main chat list page for normal users
    path('', list_chats, name='list_chats'),

    # Main chat interface view for both user types (normal user and shop owner)
    path('chats/', chats_view, name='chats_view'),  # <--- Add this line for the chats_view

    # Specific chat view with a store
    path('<int:store_id>/', chat_with_store, name='chat_with_store'),

    path('<int:store_id>/<int:customer_id>/', chat_with_cust, name="chat_with_cust"),

    # AJAX endpoint to fetch messages for a specific chat
    path('api/chats/<int:chat_id>/messages/', get_chat_messages, name='get_chat_messages'),

    # API endpoint to create a new chat with a store
    path('api/chats/create/', create_chat, name='create_chat'), 

    # API endpoint to send a message within an existing chat
    path('api/chats/<int:chat_id>/send/', send_message, name='send_message'),

    # API endpoint to get the list of stores
    path('api/stores/', get_stores, name='get_stores'),
    
    # API endpoint to delete a chat
    path('api/chats/<int:chat_id>/delete/', delete_chat, name='delete_chat'),
    
    # API endpoint to edit a message
    path('api/messages/<int:message_id>/edit/', edit_message, name='edit_message'),
]
