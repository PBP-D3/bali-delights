from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Chat, Message
from stores.models import Store
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def get_chat_messages(request, chat_id):
    # Fetch the chat
    chat = get_object_or_404(Chat, id=chat_id)

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

    context = {'chats': chat_data}
    return render(request, 'chats.html', context=context)

@login_required   
def chat_with_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    chat, created = Chat.objects.get_or_create(sender=request.user, store=store)  # Create chat if it doesn't exist
    messages = Message.objects.filter(chat=chat).order_by('timestamp')

    return render(request, 'chat_personal.html', {
        'chat': chat,
        'messages': messages,
        'store': store,
    })

@csrf_exempt
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


@login_required
def get_stores(request):
    search_query = request.GET.get('search', '')

    # Filter stores based on search query if provided
    if search_query:
        stores = Store.objects.filter(name__icontains=search_query)
    else:
        stores = Store.objects.all()

    # Prepare the data to return
    stores_data = [{'id': store.id, 'name': store.name, 'photo_url': store.photo.url if store.photo else ''} for store in stores]
    
    return JsonResponse({'stores': stores_data})

# View to render the add chat page
@login_required
def add_chat(request):
    # Load the initial store list to pass to the template if needed
    stores = Store.objects.all()
    return render(request, 'add_chat.html', {'stores': stores})

@csrf_exempt
@login_required
def create_chat(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id')
        store = get_object_or_404(Store, id=store_id)
        
        # Get or create a chat between the user and the selected store
        chat, created = Chat.objects.get_or_create(sender=request.user, store=store)
        
        return JsonResponse({'success': True, 'chat_id': chat.id})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
