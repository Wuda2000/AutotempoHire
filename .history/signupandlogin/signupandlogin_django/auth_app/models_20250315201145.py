from django.contrib.auth.models import AbstractUser, Group, Permission 
from django.db import models
from django.utils import timezone
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
    password_last_changed = models.DateTimeField(blank=True, null=True)  # ✅ Add this field
    is_active = models.BooleanField(default=False)  # ✅ Ensure email verification is required

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def save(self, *args, **kwargs):
        # Ensure password_last_changed is updated when password is changed
        if self.pk:  # Only for existing users
            old_user = CustomUser.objects.filter(pk=self.pk).first()
            if old_user and old_user.password != self.password:
                self.password_last_changed = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    from django.db import models
from users.models import User

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    qualification_years = models.IntegerField()
    location = models.CharField(max_length=100)
    payment_range = models.DecimalField(max_digits=10, decimal_places=2)
    verified = models.BooleanField(default=False)

class CarOwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=100)
