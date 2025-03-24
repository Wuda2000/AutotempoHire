import uuid
import random
from django.db import models
from django.utils.timezone import now
from auth_app.models import CustomUser

def generate_unique_id():
    """Generate a unique trip ID ensuring no duplicates."""
    while True:
        trip_id = str(random.randint(100000, 999999))
        if not Trip.objects.filter(trip_id=trip_id).exists():
            return trip_id

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Trip(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    trip_id = models.CharField(max_length=12, unique=True, primary_key=True, editable=False)
    car_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trips')
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='driven_trips')
    pickup_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_time = models.DateTimeField(default=now)
    arrival_time = models.DateTimeField(default=now)
    trip_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """Ensure trip_id is assigned before saving."""
        if not self.trip_id:
            self.trip_id = generate_unique_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Trip {self.trip_id}: {self.pickup_location} to {self.destination} by {self.driver.username if self.driver else 'Unassigned'}"
