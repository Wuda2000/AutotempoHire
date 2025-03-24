import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from auth_app.models import CustomUser  # ✅ Correctly import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser  # ✅ Ensure it references CustomUser correctly
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def clean_email(self):
        """Validate email uniqueness at the form level."""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different one.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.unique_id = uuid.uuid4().hex[:12]  # Generate a 12-character unique ID
        if commit:
            user.save()
        return user
   
class DriverForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['age', 'qualification_years', 'location', 'payment_range']

class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwnerProfile
        fields = ['car_model']

