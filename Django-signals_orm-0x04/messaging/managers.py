from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    Provides optimized queries for unread message operations.
    """
    
    def for_user(self, user):
        """
        Get all unread messages for a specific user (as receiver).
        Optimized with select_related for sender info.
        
        Args:
            user: User object to filter messages for
        
        Returns:
            QuerySet of unread messages
        """
        return self.get_queryset().filter(
            receiver=user,
            is_read=False
        ).select_related('sender', 'receiver').order_by('-timestamp')
    
    def for_user_optimized(self, user):
        """
        Get unread messages with minimal fields for inbox listing.
        Uses .only() to fetch only necessary fields, reducing memory and bandwidth.
        
        Args:
            user: User object to filter messages for
        
        Returns:
            QuerySet with only essential fields
        """
        return self.get_queryset().filter(
            receiver=user,
            is_read=False
        ).select_related('sender').only(
            # Message fields
            'id',
            'content',
            'timestamp',
            'is_read',
            'parent_message_id',  # For threading check
            # Sender fields (via select_related)
            'sender__id',
            'sender__username',
            'sender__email',
        ).order_by('-timestamp')
    
    def count_for_user(self, user):
        """
        Efficiently count unread messages for a user.
        Useful for badge counters.
        
        Args:
            user: User object
        
        Returns:
            Integer count of unread messages
        """
        return self.get_queryset().filter(
            receiver=user,
            is_read=False
        ).count()
    
    def root_messages_for_user(self, user):
        """
        Get unread root messages (thread starters) for a user.
        Useful for showing unread threads.
        
        Args:
            user: User object
        
        Returns:
            QuerySet of unread root messages
        """
        return self.get_queryset().filter(
            receiver=user,
            is_read=False,
            parent_message__isnull=True  # Only root messages
        ).select_related('sender').order_by('-timestamp')
    
    def mark_as_read(self, message_ids):
        """
        Bulk mark messages as read.
        More efficient than updating one by one.
        
        Args:
            message_ids: List of message IDs to mark as read
        
        Returns:
            Number of messages updated
        """
        return self.get_queryset().filter(
            id__in=message_ids
        ).update(is_read=True)


class ReadMessagesManager(models.Manager):
    """
    Custom manager for read messages.
    Provides queries for message history/archive.
    """
    
    def for_user(self, user):
        """
        Get all read messages for a user.
        
        Args:
            user: User object
        
        Returns:
            QuerySet of read messages
        """
        return self.get_queryset().filter(
            receiver=user,
            is_read=True
        ).select_related('sender').order_by('-timestamp')
    
    def for_user_optimized(self, user):
        """
        Get read messages with minimal fields for archive listing.
        
        Args:
            user: User object
        
        Returns:
            QuerySet with only essential fields
        """
        return self.get_queryset().filter(
            receiver=user,
            is_read=True
        ).select_related('sender').only(
            'id',
            'content',
            'timestamp',
            'sender__id',
            'sender__username'
        ).order_by('-timestamp')