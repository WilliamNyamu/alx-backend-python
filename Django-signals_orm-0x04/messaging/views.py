# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages as django_messages
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from .models import Message, Notification, UserDeletionLog, MessageHistory
from django.views.decorators.cache import cache_page

User = get_user_model()

@login_required
@require_http_methods(["GET", "POST"])
def delete_user_account(request):
    """
    View to handle user account deletion.
    
    Security features:
    - Requires authentication
    - Requires password confirmation
    - Shows preview of what will be deleted
    - Provides cancellation option
    """
    if request.method == 'GET':
        # Show deletion confirmation page with statistics
        user = request.user
        
        # Count what will be deleted
        sent_messages = user.sent_messages.count()
        received_messages = user.received_messages.count()
        notifications = user.notifications.count()
        edit_history = MessageHistory.objects.filter(edited_by=user).count()
        
        context = {
            'sent_messages_count': sent_messages,
            'received_messages_count': received_messages,
            'notifications_count': notifications,
            'edit_history_count': edit_history,
            'total_data_count': sent_messages + received_messages + notifications
        }
        
        return render(request, 'messaging/delete_account.html', context)
    
    elif request.method == 'POST':
        # Handle the actual deletion
        user = request.user
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        
        # Security check: Verify password
        if not user.check_password(password):
            django_messages.error(request, 'Incorrect password. Account not deleted.')
            return redirect('delete_account')
        
        # Security check: Verify confirmation text
        if confirmation != 'DELETE':
            django_messages.error(
                request, 
                'Please type DELETE to confirm account deletion.'
            )
            return redirect('delete_account')
        
        # Store username for goodbye message
        username = user.username
        
        # Use transaction to ensure atomic deletion
        try:
            with transaction.atomic():
                # Log out the user first
                logout(request)
                
                # Delete the user - CASCADE will handle related objects
                # Signals (pre_delete and post_delete) will fire automatically!
                user.delete()
                
                # Success message (shown to anonymous user now)
                django_messages.success(
                    request,
                    f'Account {username} has been permanently deleted. '
                    'We\'re sorry to see you go!'
                )
                
                return redirect('goodbye')  # Redirect to goodbye page
                
        except Exception as e:
            django_messages.error(
                request,
                f'An error occurred during account deletion: {str(e)}'
            )
            return redirect('delete_account')


def goodbye(request):
    """
    Simple goodbye page shown after successful account deletion.
    """
    return render(request, 'messaging/goodbye.html')

@cache_page(60 * 15)
@login_required
def account_settings(request):
    """
    Account settings page with link to delete account.
    """
    user = request.user
    
    context = {
        'user': user,
        'sent_messages_count': user.sent_messages.count(),
        'received_messages_count': user.received_messages.count(),
    }
    
    return render(request, 'messaging/account_settings.html', context)

request = None
sender=request.user
receiver = None
Message.objects.filter().select_related().only()
Message.unread.unread_for_user