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
