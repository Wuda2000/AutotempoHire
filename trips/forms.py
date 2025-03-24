from django import forms
from .models import Trip, User  


class TripBookingForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'pickup_location', 'trip_date', 'price', 'car_owner', 'driver']
        widgets = {
            'trip_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the User model has a 'role' field
        self.fields['driver'].queryset = User.objects.filter(role='Driver')  # Ensure role matches stored values
        self.fields['car_owner'].queryset = User.objects.filter(role='CarOwner') 


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True}),
            'email': forms.EmailInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True  
