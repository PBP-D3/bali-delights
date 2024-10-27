from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Chat, Message
from stores.models import Store
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Max

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
            'id': message.id,  # Include the message ID here
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sender_is_user': message.sender == request.user,  # Check if the sender is the current user
        })

    return JsonResponse({'messages': message_data})


@login_required
def list_chats(request):
    user = request.user
    chats = Chat.objects.filter(sender=user) \
        .annotate(last_message_time=Max('messages__timestamp')) \
        .order_by('-last_message_time')

    chat_data = []
    for chat in chats:
        store = chat.store
        # Get the last message content, if it exists
        last_message = Message.objects.filter(chat=chat).order_by('-timestamp').first()
        
        chat_data.append({
            'store': {
                'id': store.id,
                'name': store.name,
                'photo_url': store.photo if store.photo else '/static/images/default_avatar.jpg',
            },
            'last_message_time': chat.last_message_time.strftime('%Y-%m-%d %H:%M:%S') if chat.last_message_time else "No messages",
            'last_message_content': last_message.content if last_message else ""
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

@login_required
@csrf_exempt
def send_message(request, chat_id):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        chat = Chat.objects.get(id=chat_id)
        message = Message.objects.create(chat=chat, sender=request.user, content=message_content)
        return JsonResponse({
            "success": True,
            "message": {
                "content": message.content
            }
        })
    return JsonResponse({"success": False}, status=400)

@login_required
def get_stores(request):
    search_query = request.GET.get('search', '')

    # Retrieve all stores or filter by search query
    if search_query:
        stores = Store.objects.filter(name__icontains=search_query)
    else:
        stores = Store.objects.all()

    # Prepare the data to return
    stores_data = [
        {
            'id': store.id,
            'name': store.name,
            'photo_url': store.photo if isinstance(store.photo, str) else store.photo.url if store.photo else '/static/images/default_avatar.jpg'
        }
        for store in stores
    ]
    
    return JsonResponse({'stores': stores_data})

@login_required
@csrf_exempt
def create_chat(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id')
        store = get_object_or_404(Store, id=store_id)

        # Check if a chat already exists with this store
        chat, created = Chat.objects.get_or_create(sender=request.user, store=store)

        # Return the chat ID so the frontend can redirect
        return JsonResponse({'success': True, 'chat_id': chat.id})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
@csrf_exempt
def delete_chat(request, chat_id):
    if request.method == "POST":
        try:
            chat = get_object_or_404(Chat, id=chat_id, sender=request.user)
            chat.delete()
            return JsonResponse({"success": True})
        except Chat.DoesNotExist:
            return JsonResponse({"success": False, "error": "Chat does not exist."}, status=404)
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

@login_required
@csrf_exempt
def edit_message(request, message_id):
    if request.method == 'POST':
        new_content = request.POST.get('content', '').strip()

        if not new_content:
            print("Edit failed: Content is empty.")
            return JsonResponse({"success": False, "error": "Content cannot be empty."}, status=400)

        try:
            # Ensure the message exists and the user has permission to edit it
            message = get_object_or_404(Message, id=message_id, sender=request.user)
            message.content = new_content
            message.save()
            print("Message edited successfully.")
            return JsonResponse({"success": True})
        
        except Exception as e:
            print(f"Error in edit_message view: {e}")  # This will log the exact issue in the console
            return JsonResponse({"success": False, "error": "Server error occurred"}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)