from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

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

    def __str__(self):
        return self.username

class DriverApplication(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # ✅ Fixed User reference
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    age = models.IntegerField()
    ethnicity = models.CharField(max_length=20, choices=[
        ('Kikuyu', 'Kikuyu'), ('Luo', 'Luo'), ('Luhya', 'Luhya'),
        ('Kalenjin', 'Kalenjin'), ('Kamba', 'Kamba'), ('Other', 'Other')
    ])
    years_of_experience = models.IntegerField()
    kcse_certificate = models.FileField(upload_to='driver_documents/')
    good_conduct = models.FileField(upload_to='driver_documents/')
    cover_letter = models.FileField(upload_to='driver_documents/')
    cv = models.FileField(upload_to='driver_documents/')
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username  # ✅ Corrected __str__() method
