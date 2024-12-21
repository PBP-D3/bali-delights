from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Chat, Message
from stores.models import Store  # Adjust the import if the module path is correct
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Max
from django.utils.html import strip_tags


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
            'id': message.id,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sender_is_user': message.sender == request.user,
        })

    return JsonResponse({'messages': message_data})

@login_required
def list_chats(request):
    user = request.user
    chat_data = []

    if user.role == "shop_owner":
        # If the user is a shop owner, get stores they own
        owned_stores = Store.objects.filter(owner_id=user.id)
        
        # Get chats associated with these stores
        chats = Chat.objects.filter(store__in=owned_stores).annotate(last_message_time=Max('messages__timestamp')).order_by('-last_message_time')
        
        for chat in chats:
            # Get the last message content and user details
            last_message = Message.objects.filter(chat=chat).order_by('-timestamp').first()
            chat_data.append({
                'id':chat.id,
                'user': {
                    'id': chat.sender.id,
                    'username': chat.sender.username,
                },
                'store': {
                    'id': chat.store.id,
                },
                'last_message_time': chat.last_message_time.strftime('%Y-%m-%d %H:%M:%S') if chat.last_message_time else "No messages",
                'last_message_content': last_message.content if last_message else ""
            })

    else:
        # For normal users, get chats they initiated
        chats = Chat.objects.filter(sender=user).annotate(last_message_time=Max('messages__timestamp')).order_by('-last_message_time')
        
        for chat in chats:
            # Get the last message content
            last_message = Message.objects.filter(chat=chat).order_by('-timestamp').first()
            chat_data.append({
                'id':chat.id,
                'store': {
                    'id': chat.store.id,
                    'name': chat.store.name,
                    'photo_url': chat.store.get_image if chat.store.get_image else '/static/images/default_avatar.jpg',
                },
                'last_message_time': chat.last_message_time.strftime('%Y-%m-%d %H:%M:%S') if chat.last_message_time else "No messages",
                'last_message_content': last_message.content if last_message else ""
            })

    context = {'chats': chat_data}
    return render(request, 'chats.html', context=context)

def chat_with_cust(request, store_id, customer_id):
    store = get_object_or_404(Store, id=store_id)
    cust = get_object_or_404(User, id=customer_id)

    chat, created = Chat.objects.get_or_create(store=store, sender=cust)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')

    return render(request, 'chat_personal.html', {
        'chat': chat,
        'messages': messages,
        'store': store,
        'cust_name': cust.username,
    })

@login_required
def chat_with_store(request, store_id):
    # Retrieve the store based on the provided store ID and make sure it matches the owner (logged-in user)
    store = get_object_or_404(Store, id=store_id)

    # Retrieve or create a chat between the logged-in user and the store
    chat, created = Chat.objects.get_or_create(sender=request.user, store=store)
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
        message_content = strip_tags(request.POST.get('message'))
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
    search_query = strip_tags(request.GET.get('search', ''))
    print(search_query)

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
            'photo_url': store.get_image() 
        }
        for store in stores
    ]
    
    return JsonResponse({'stores': stores_data})

@login_required
@csrf_exempt
def create_chat(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id')
        print(store_id)
        store = get_object_or_404(Store, id=store_id)
        print(store.name)
        
        # Membuat atau mendapatkan chat yang sudah ada
        chat, created = Chat.objects.get_or_create(sender=request.user, store=store)
        
        # Return the chat ID so the frontend can redirect
        return JsonResponse({'success': True, 'store_id': store.id})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
@csrf_exempt
def delete_chat(request, chat_id):
    print(chat_id)
    if request.method == "POST":
        try:
            chat = get_object_or_404(Chat, id=chat_id)
            chat.delete()
            return JsonResponse({"success": True})
        except Chat.DoesNotExist:
            return JsonResponse({"success": False, "error": "Chat does not exist."}, status=404)
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

@login_required
@csrf_exempt
def edit_message(request, message_id):
    if request.method == 'POST':
        new_content = strip_tags(request.POST.get('content', '')).strip()

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
            print(f"Error in edit_message view: {e}")
            return JsonResponse({"success": False, "error": "Server error occurred"}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@login_required
def chats_view(request):
    user = request.user
    chats = None

    if user.role == "shop_owner":
        # Retrieve all stores owned by this shop owner
        owner_stores = Store.objects.filter(owner=user)  # Retrieve stores based on the owner's ID
        # Retrieve all chats associated with these stores
        chats = Chat.objects.filter(store__in=owner_stores).select_related('sender', 'store')
    else:
        # For normal users, retrieve only the chats they initiated
        chats = Chat.objects.filter(sender=user).select_related('store')

    context = {
        'chats': chats,
        'user': user
    }
    return render(request, 'chats.html', context)