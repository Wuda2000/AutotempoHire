import uuid  # For generating unique IDs
from django.db import models
from django.utils import timezone  # Fix timezone error
from auth_app.models import CustomUser as User


def generate_unique_id():
    """Generates a unique 12-character trip ID."""
    return uuid.uuid4().hex[:12]


class Trip(models.Model):
    trip_id = models.CharField(max_length=255, unique=True, blank=True, null=True)  # Added trip_id field

    """
    Stores trip details, including the driver, car owner, trip location, and status.
    Also includes fields for real-time tracking.
    """
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="driver_trips")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_trips")
    destination = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    trip_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, 
        choices=[('ongoing', 'Ongoing'), ('completed', 'Completed'), ('canceled', 'Canceled')],
        default='ongoing'
    )

    def save(self, *args, **kwargs):
        if not self.trip_id:
            self.trip_id = generate_unique_id()  # Ensure trip_id is assigned
        if self.trip_date and not self.trip_date.tzinfo:
            self.trip_date = timezone.make_aware(self.trip_date)  # Ensure timezone
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Trip from {self.pickup_location} to {self.destination} ({self.status})"


class TrackingModel(models.Model):
    """
    Stores real-time location updates for users (drivers and car owners).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Location of {self.user.username} (Lat: {self.latitude}, Long: {self.longitude})"
