from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import CustomUser, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """Create a new conversation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message to an existing conversation"""
        conversation = self.get_object()
        
        message_data = {
            'sender_id': request.data.get('sender_id'),
            'message_body': request.data.get('message_body'),
            'conversation': conversation.conversation_id
        }
        
        serializer = MessageSerializer(data=message_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """List all messages in a conversation"""
        conversation = self.get_object()
        messages = Message.objects.filter(conversation=conversation).order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all().order_by('-sent_at')
        conversation_id = self.request.query_params.get('conversation_id')
        sender_id = self.request.query_params.get('sender_id')
        
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        if sender_id:
            queryset = queryset.filter(sender_id=sender_id)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a new message"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)