# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    """
    Message model with edit tracking
    """
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    # NEW: Edit tracking fields
    edited = models.BooleanField(default=False)
    last_edited_at = models.DateTimeField(null=True, blank=True)
    edit_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['receiver', '-timestamp']),
        ]
    
    def __str__(self):
        edit_status = " (edited)" if self.edited else ""
        return f"From {self.sender.username} to {self.receiver.username}{edit_status}"
    
    def get_edit_history(self):
        """Helper method to retrieve all edit history for this message"""
        return self.edit_history.all().order_by('-edited_at')
    
    def has_been_edited(self):
        """Check if message has edit history"""
        return self.edit_history.exists()


class MessageHistory(models.Model):
    """
    Stores the history of message edits.
    Each time a message is edited, the OLD content is saved here.
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='edit_history'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='message_edits'
    )
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name = 'Message History'
        verbose_name_plural = 'Message Histories'
        indexes = [
            models.Index(fields=['message', '-edited_at']),
        ]
    
    def __str__(self):
        return f"Edit of message {self.message.id} at {self.edited_at}"
    
    def content_preview(self):
        """Return a preview of the old content"""
        return self.old_content[:100] + '...' if len(self.old_content) > 100 else self.old_content


class Notification(models.Model):
    """
    Notification model (keeping from previous exercise)
    """
    NOTIFICATION_TYPES = (
        ('new_message', 'New Message'),
        ('message_read', 'Message Read'),
        ('message_edited', 'Message Edited'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
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
