from django import forms
from .models import DriverProfile, CarOwnerProfile

class DriverForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['age', 'qualification_years', 'location', 'payment_range']

class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwnerProfile
        fields = ['car_model']
