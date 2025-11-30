# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    """
    Message model with CASCADE delete behavior and threading support
    """
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # When user deleted, delete their sent messages
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # When user deleted, delete their received messages
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    last_edited_at = models.DateTimeField(null=True, blank=True)
    edit_count = models.PositiveIntegerField(default=0)
    
    # NEW: Self-referential foreign key for threaded replies
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,  # When parent deleted, delete all replies
        null=True,
        blank=True,
        related_name='replies'  # Access replies via message.replies.all()
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['receiver', '-timestamp']),
            models.Index(fields=['parent_message', '-timestamp']),  # Index for reply queries
        ]
    
    def __str__(self):
        reply_indicator = " (Reply)" if self.parent_message else ""
        return f"From {self.sender.username} to {self.receiver.username}{reply_indicator}"
    
    def is_reply(self):
        """Check if this message is a reply to another message"""
        return self.parent_message is not None
    
    def is_thread_starter(self):
        """Check if this message started a thread (has replies)"""
        return self.replies.exists()
    
    def get_thread_depth(self):
        """Calculate how deep this message is in the thread (0 = root)"""
        depth = 0
        current = self
        while current.parent_message:
            depth += 1
            current = current.parent_message
        return depth
    
    def get_root_message(self):
        """Get the root message of this thread"""
        current = self
        while current.parent_message:
            current = current.parent_message
        return current
    
    def get_all_replies_recursive(self):
        """
        Recursively fetch all replies (direct and nested).
        Returns a flat list of all descendant messages.
        """
        all_replies = []
        
        def collect_replies(message):
            # Get direct replies with optimized query
            direct_replies = message.replies.select_related(
                'sender', 'receiver', 'parent_message'
            ).all()
            
            for reply in direct_replies:
                all_replies.append(reply)
                # Recursively collect nested replies
                collect_replies(reply)
        
        collect_replies(self)
        return all_replies
    
    def get_reply_count(self):
        """Get total number of replies (direct + nested)"""
        return len(self.get_all_replies_recursive())
    
    def get_thread_messages(self):
        """
        Get all messages in this thread (root + all replies).
        Returns messages in chronological order.
        """
        root = self.get_root_message()
        thread_messages = [root] + root.get_all_replies_recursive()
        return sorted(thread_messages, key=lambda m: m.timestamp)
    
    @classmethod
    def get_root_messages_with_replies(cls, user=None):
        """
        Optimized query to fetch root messages with their replies.
        Uses prefetch_related to minimize database queries.
        
        Args:
            user: Optional User to filter messages (sent or received)
        
        Returns:
            QuerySet of root messages with replies prefetched
        """
        queryset = cls.objects.filter(parent_message__isnull=True)
        
        if user:
            queryset = queryset.filter(
                models.Q(sender=user) | models.Q(receiver=user)
            )
        
        # Prefetch all related data in minimal queries
        return queryset.select_related(
            'sender', 'receiver'
        ).prefetch_related(
            models.Prefetch(
                'replies',
                queryset=cls.objects.select_related('sender', 'receiver').order_by('timestamp')
            )
        ).order_by('-timestamp')
    
    @classmethod
    def get_thread_optimized(cls, root_message_id):
        """
        Fetch an entire thread with optimized queries.
        Gets root message and all nested replies efficiently.
        
        Args:
            root_message_id: ID of the root message
        
        Returns:
            Root message with all replies prefetched
        """
        return cls.objects.filter(
            pk=root_message_id
        ).select_related(
            'sender', 'receiver'
        ).prefetch_related(
            models.Prefetch(
                'replies',
                queryset=cls.objects.select_related(
                    'sender', 'receiver', 'parent_message'
                ).prefetch_related('replies')  # Nested prefetch for multi-level replies
            )
        ).first()
    
    def get_replies_tree(self):
        """
        Get replies in a tree structure for threaded display.
        Returns list of tuples: (message, depth_level)
        """
        tree = []
        
        def build_tree(message, depth=0):
            # Add current message with its depth
            tree.append((message, depth))
            # Recursively add replies
            for reply in message.replies.all():
                build_tree(reply, depth + 1)
        
        # Start from direct replies
        for reply in self.replies.all():
            build_tree(reply, depth=1)
        
        return tree


class MessageHistory(models.Model):
    """
    Message edit history with CASCADE delete
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,  # When message deleted, delete its history
        related_name='edit_history'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Keep history even if editor deleted
        null=True,
        related_name='message_edits'
    )
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = 'Message Histories'
    
    def __str__(self):
        return f"Edit of message {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    """
    Notification model with CASCADE delete
    """
    NOTIFICATION_TYPES = (
        ('new_message', 'New Message'),
        ('message_read', 'Message Read'),
        ('message_edited', 'Message Edited'),
        ('account_deletion', 'Account Deletion'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # When user deleted, delete their notifications
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,  # When message deleted, delete its notifications
        related_name='notifications',
        null=True,
        blank=True
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='new_message'
    )
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.content}"


class UserDeletionLog(models.Model):
    """
    Optional: Log user deletions for audit purposes
    Stores information AFTER user is deleted
    """
    username = models.CharField(max_length=150)
    email = models.EmailField()
    date_joined = models.DateTimeField()
    deleted_at = models.DateTimeField(auto_now_add=True)
    messages_sent_count = models.IntegerField(default=0)
    messages_received_count = models.IntegerField(default=0)
    notifications_count = models.IntegerField(default=0)
    deletion_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-deleted_at']
    
    def __str__(self):
        return f"Deleted user: {self.username} on {self.deleted_at}"
