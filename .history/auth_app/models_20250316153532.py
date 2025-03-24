from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now
import uuid

def generate_unique_id():
    return uuid.uuid4().hex[:12]  # Ensures each user gets a unique ID

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('carOwner', 'Car Owner'),
        ('driver', 'Driver'),
    ]

    unique_id = models.CharField(
        max_length=12,
        unique=True,
        default=generate_unique_id,
        editable=False
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    password_reset_token = models.CharField(max_length=32, blank=True, null=True)
    password_last_changed = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Email verification required

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    USERNAME_FIELD = "username"  # ✅ Ensure Django uses username for login
    REQUIRED_FIELDS = ["email"]  # ✅ Superuser requires email

    def save(self, *args, **kwargs):
        """Ensure password is hashed before saving"""
        if not self.password.startswith('pbkdf2_sha256$'):  # ✅ Prevent re-hashing an already hashed password
            self.set_password(self.password)  

        if self.pk:  # ✅ Track when password was last changed
            old_user = CustomUser.objects.filter(pk=self.pk).first()
            if old_user and old_user.password != self.password:
                self.password_last_changed = now()

        super().save(*args, **kwargs)  # ✅ Correct super() call

    def __str__(self):
        return self.username
