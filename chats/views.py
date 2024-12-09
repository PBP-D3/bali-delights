from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from django.utils.timezone import localtime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from .models import Chat, Message
from stores.models import Store
from .serializers import ChatSerializer, MessageSerializer

User = get_user_model()

@api_view(['GET'])
@login_required
def get_chat_messages(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response({'messages': serializer.data})


@api_view(['GET'])
@login_required
def list_chats(request):
    user = request.user

    if user.role == "shop_owner":
        owned_stores = Store.objects.filter(owner=user)
        chats = Chat.objects.filter(store__in=owned_stores).order_by('-created_at')
    else:
        chats = Chat.objects.filter(sender=user).order_by('-created_at')

    serializer = ChatSerializer(chats, many=True)
    return Response({'chats': serializer.data})


@api_view(['POST'])
@login_required
def chat_with_cust(request, store_id, customer_id):
    store = get_object_or_404(Store, id=store_id)
    cust = get_object_or_404(User, id=customer_id)

    chat, created = Chat.objects.get_or_create(store=store, sender=cust)
    serializer = ChatSerializer(chat)
    return Response(serializer.data)


@api_view(['POST'])
@login_required
def chat_with_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    chat, created = Chat.objects.get_or_create(sender=request.user, store=store)
    serializer = ChatSerializer(chat)
    return Response(serializer.data)


@api_view(['POST'])
@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    message_content = strip_tags(request.data.get('message', ''))

    if not message_content:
        return Response({"success": False, "error": "Message content cannot be empty."}, status=HTTP_400_BAD_REQUEST)

    message = Message.objects.create(chat=chat, sender=request.user, content=message_content)
    serializer = MessageSerializer(message)
    return Response({"success": True, "message": serializer.data})


@api_view(['GET'])
@login_required
def get_stores(request):
    search_query = request.query_params.get('search', '')
    if search_query:
        stores = Store.objects.filter(name__icontains=search_query)
    else:
        stores = Store.objects.all()

    stores_data = [
        {
            'id': store.id,
            'name': store.name,
            'photo_url': store.get_image() or '/static/images/default_avatar.jpg',
        }
        for store in stores
    ]
    return Response({'stores': stores_data})


@api_view(['POST'])
@login_required
def create_chat(request):
    store_id = request.data.get('store_id')
    store = get_object_or_404(Store, id=store_id)

    chat, created = Chat.objects.get_or_create(sender=request.user, store=store)
    return Response({'success': True, 'store_id': store.id, 'chat_id': chat.id})


@api_view(['POST'])
@login_required
def delete_chat(request, chat_id):
    try:
        chat = get_object_or_404(Chat, id=chat_id)
        chat.delete()
        return Response({"success": True})
    except Chat.DoesNotExist:
        return Response({"success": False, "error": "Chat does not exist."}, status=HTTP_404_NOT_FOUND)


@api_view(['POST'])
@login_required
def edit_message(request, message_id):
    new_content = strip_tags(request.data.get('content', '')).strip()

    if not new_content:
        return Response({"success": False, "error": "Content cannot be empty."}, status=HTTP_400_BAD_REQUEST)

    message = get_object_or_404(Message, id=message_id, sender=request.user)
    message.content = new_content
    message.save()
    return Response({"success": True})


@api_view(['GET'])
@login_required
def chats_view(request):
    user = request.user

    if user.role == "shop_owner":
        owner_stores = Store.objects.filter(owner=user)
        chats = Chat.objects.filter(store__in=owner_stores).select_related('sender', 'store')
    else:
        chats = Chat.objects.filter(sender=user).select_related('store')

    serializer = ChatSerializer(chats, many=True)
    return Response({'chats': serializer.data})
