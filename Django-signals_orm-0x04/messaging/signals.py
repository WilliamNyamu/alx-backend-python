# signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, MessageHistory, Notification


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    PRE_SAVE Signal: Captures the OLD content before a message is updated.
    
    This fires BEFORE the message is saved to the database, allowing us
    to compare the old content with the new content.
    
    Key Concept: We fetch the OLD version from database and compare with
    the NEW version that's about to be saved.
    """
    # Only process if this is an UPDATE (not a new message)
    if instance.pk:  # pk exists = message already in database
        try:
            # Fetch the OLD version from database
            old_message = Message.objects.get(pk=instance.pk)
            
            # Check if content has actually changed
            if old_message.content != instance.content:
                # Save the OLD content to history before it's lost!
                MessageHistory.objects.create(
                    message=instance,  # Link to the message being edited
                    old_content=old_message.content,  # Store OLD content
                    edited_by=instance.sender  # Who made the edit
                )
                
                # Update the message's edit tracking fields
                instance.edited = True
                instance.last_edited_at = timezone.now()
                instance.edit_count = old_message.edit_count + 1
                
                print(f"📝 Message edit logged! Version {instance.edit_count}")
                
        except Message.DoesNotExist:
            # This shouldn't happen, but handle gracefully
            pass


@receiver(post_save, sender=Message)
def notify_receiver_of_edit(sender, instance, created, **kwargs):
    """
    POST_SAVE Signal: Notify the receiver when a message is edited.
    
    This fires AFTER the message is saved, so we can safely check
    if it was edited and create a notification.
    """
    # Only notify if message was edited (not newly created)
    if not created and instance.edited:
        # Check if we already notified about this specific edit
        # (to avoid duplicate notifications)
        recent_edit_notification = Notification.objects.filter(
            user=instance.receiver,
            message=instance,
            notification_type='message_edited',
            created_at__gte=timezone.now() - timezone.timedelta(seconds=5)
        ).exists()
        
        if not recent_edit_notification:
            Notification.objects.create(
                user=instance.receiver,
                message=instance,
                notification_type='message_edited',
                content=f"{instance.sender.username} edited their message"
            )
            print(f"🔔 Edit notification sent to {instance.receiver.username}")


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    POST_SAVE Signal: Create notification for new messages.
    (Keeping from previous exercise)
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type='new_message',
            content=f"New message from {instance.sender.username}"
        )
