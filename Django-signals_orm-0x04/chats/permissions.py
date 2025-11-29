## Permissions for the chat
from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsConversationParticipant(BasePermission):
    PUT = None
    PATCH=None
    DELETE=None
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated()