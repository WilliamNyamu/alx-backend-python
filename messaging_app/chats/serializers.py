from rest_framework import serializers
from .models import CustomUser, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number', 'role']
        read_only_fields = ['user_id']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(source='sender_id', read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        write_only=True
    )

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_id', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(source='participants_id', read_only=True)
    participants_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        write_only=True
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participants_id', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']