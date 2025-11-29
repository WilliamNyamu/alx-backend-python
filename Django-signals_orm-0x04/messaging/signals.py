# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal handler that creates a notification when a new message is created.
    
    Args:
        sender: The Message model class
        instance: The actual Message instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments (always include this!)
    """
    # Only create notification for new messages, not updates
    if created:
        # Create notification for the receiver
        notification_content = f"New message from {instance.sender.username}"
        
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type='new_message',
            content=notification_content
        )
        
        print(f"📬 Notification created for {instance.receiver.username}")


@receiver(post_save, sender=Message)
def notify_sender_on_message_read(sender, instance, created, **kwargs):
    """
    Optional: Create notification for sender when their message is read.
    This demonstrates multiple signals listening to the same model.
    """
    # Only trigger if message was updated (not created) and is_read changed to True
    if not created and instance.is_read:
        # Check if notification already exists to avoid duplicates
        existing_notification = Notification.objects.filter(
            user=instance.sender,
            message=instance,
            notification_type='message_read'
        ).exists()
        
        if not existing_notification:
            notification_content = f"{instance.receiver.username} read your message"
            
            Notification.objects.create(
                user=instance.sender,
                message=instance,
                notification_type='message_read',
                content=notification_content
            )
            
            print(f"✅ Read notification created for {instance.sender.username}")
