from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'  # Replace with your app name
    
    def ready(self):
        """
        Import signals when the app is ready.
        This ensures signals are registered when Django starts.
        """
        import messaging.signals