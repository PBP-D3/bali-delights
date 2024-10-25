from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from store.models import Store
from django.http import JsonResponse

@login_required
def get_chat_messages(request, chat_id):
    # Fetch the chat
    chat = Chat.objects.get(id=chat_id)

    # Get all messages related to the chat
    messages = Message.objects.filter(chat=chat).order_by('timestamp')

    message_data = []
    for message in messages:
        message_data.append({
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sender_is_user': message.sender == request.user,  # Check if the sender is the current user
        })

    return JsonResponse({'messages': message_data})

@login_required
def list_chats(request):
    user = request.user
    chats = Chat.objects.filter(sender=user)  # Assuming `sender` is the user

    # Prepare data for the response
    chat_data = []
    for chat in chats:
        store = chat.store
        chat_data.append({
            'store': {
                'id': store.id,
                'name': store.name,
                'photo_url': store.photo.url if store.photo else '/static/images/default_avatar.jpg',  # Default image if no photo
            },
            'last_message_time': chat.messages.last().timestamp.strftime('%Y-%m-%d %H:%M:%S') if chat.messages.exists() else "No messages"
        })

    return JsonResponse({'chats': chat_data})

@login_required   
def chat_with_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    chat = get_object_or_404(Chat, sender=request.user, store=store)  # Use get_object_or_404 for consistency
    messages = Message.objects.filter(chat=chat).order_by('timestamp')

    return render(request, 'chat_personal.html', {
        'chat': chat,
        'messages': messages,
        'store': store,
    })

@login_required
def send_message(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, id=chat_id)
        message_content = request.POST.get('message')

        # Create and save the new message
        if message_content:
            message = Message.objects.create(
                chat=chat,
                sender=request.user,
                content=message_content
            )
            # Return JSON response with message data
            return JsonResponse({
                'success': True,
                'message': {
                    'content': message.content,
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'sender_is_user': True
                }
            })
        return JsonResponse({'success': False, 'error': 'Empty message content'}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
