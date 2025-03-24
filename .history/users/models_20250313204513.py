from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    ROLE_CHOICES = [
        ('car_owner', 'Car Owner'),
        ('driver', 'Driver'),
    ]
    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # Admin approval

    def __str__(self):
        return self.username
