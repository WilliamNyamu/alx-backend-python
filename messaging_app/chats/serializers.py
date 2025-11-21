from rest_framework import serializers
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        pass

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        pass

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        pass