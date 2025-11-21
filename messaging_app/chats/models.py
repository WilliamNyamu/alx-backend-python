from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid
# Create your models here.

class CustomManager(UserManager):
    """Custom auth manager that uses email as the default authentication"""
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('issuperuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin')
    ]
    phone_number = models.CharField(max_length=10, null=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, null=False)

    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=10, null=False)
    
    email = models.EmailField(unique=True, null=False)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now=True)

