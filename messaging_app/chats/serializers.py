from rest_framework import serializers
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number', 'role']

class MessageSerializer(serializers.ModelSerializer):
    sender_id = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'message_id', 'sender_id', 'sent_at']
        read_only_fields = ['sent_at']
    

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at']