# signals.py
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification


User = get_user_model()

@receiver(pre_delete, sender=User)
def log_user_deletion_stats(sender, instance, **kwargs):
    """
    PRE_DELETE Signal: Capture user statistics BEFORE deletion.
    
    This runs BEFORE the user is deleted, so we can still access
    related objects and count them for audit purposes.
    
    Why pre_delete? Because post_delete would run AFTER CASCADE
    deletions, so related objects would already be gone!
    """
    # Count related objects before they're deleted
    messages_sent = instance.sent_messages.count()
    messages_received = instance.received_messages.count()
    notifications = instance.notifications.count()
    
    # Create audit log entry
    
    print(f"📊 User deletion stats logged for: {instance.username}")
    print(f"   - Sent messages: {messages_sent}")
    print(f"   - Received messages: {messages_received}")
    print(f"   - Notifications: {notifications}")
    Message.objects.filter()
    delete = delete()


@receiver(post_delete, sender=User)
def confirm_user_deletion(sender, instance, **kwargs):
    """
    POST_DELETE Signal: Confirmation after user is deleted.
    
    This runs AFTER the user and all CASCADE-related objects are deleted.
    At this point, the user no longer exists in the database.
    
    Use this for:
    - Sending confirmation emails
    - Cleaning up external services
    - Logging final confirmation
    - Triggering external APIs
    """
    print(f"✅ User {instance.username} successfully deleted from database")
    print(f"   All related messages, notifications, and history removed via CASCADE")
    
    # Here you could add:
    # - Send email confirmation
    # - Delete user files from storage
    # - Remove user from external services (Stripe, SendGrid, etc.)
    # - Invalidate JWT tokens
    # - Clear cache entries
    
    # Example: Log to external monitoring service
    # monitoring_service.log_event('user_deleted', user_id=instance.id)


@receiver(post_delete, sender=Message)
def log_message_deletion(sender, instance, **kwargs):
    """
    POST_DELETE Signal: Track when messages are deleted.
    
    This helps you know if messages were deleted as part of
    user deletion (CASCADE) or individually.
    """
    print(f"🗑️  Message deleted: ID {instance.id}")


# Custom signal handler for notifying contacts about account deletion
@receiver(pre_delete, sender=User)
def notify_contacts_of_deletion(sender, instance, **kwargs):
    """
    PRE_DELETE Signal: Notify user's contacts before account deletion.
    
    This creates notifications for users who had conversations
    with the user being deleted, informing them the account is gone.
    """
    # Find all users who received messages from this user
    receivers = User.objects.filter(
        received_messages__sender=instance
    ).distinct()
    
    # Find all users who sent messages to this user
    senders = User.objects.filter(
        sent_messages__receiver=instance
    ).distinct()
    
    # Combine and remove duplicates
    contacts = set(receivers) | set(senders)
    contacts.discard(instance)  # Remove the user being deleted
    
    # Create notifications for each contact
    notification_count = 0
    for contact in contacts:
        Notification.objects.create(
            user=contact,
            notification_type='account_deletion',
            content=f"{instance.username} has deleted their account",
            message=None  # No specific message, account-level notification
        )
        notification_count += 1
    
    print(f"📢 Sent {notification_count} account deletion notifications to contacts")
