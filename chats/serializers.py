from rest_framework import serializers
from .models import Chat, Message
from stores.models import Store  # Import Store jika perlu

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'sender_username', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class ChatSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'sender', 'sender_username', 'store', 'store_name', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at', 'messages']
