from rest_framework.routers import NestedDefaultRouter, DefaultRouter
from .views import UserViewSet, ConversationViewSet, MessageViewSet
from django.urls import path, include

router = DefaultRouter()
router = NestedDefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = router.urls