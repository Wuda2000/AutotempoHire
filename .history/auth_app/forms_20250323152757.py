import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from auth_app.models import CustomUser  # ✅ Correctly import CustomUser
from .models import DriverApplication

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser  # ✅ Ensure it references CustomUser correctly
        fields = ('username', 'email', 'password1', 'password2', 'role')


class DriverApplicationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 21}))

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        if age and age < 21:
            self.add_error('age', "You must be at least 21 years old to apply.")
    ethnicity = forms.ChoiceField(
        choices=[('Kikuyu', 'Kikuyu'), ('Luo', 'Luo'), ('Luhya', 'Luhya'), ('Kalenjin', 'Kalenjin'), ('Kamba', 'Kamba'), ('Other', 'Other')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    kcse_certificate = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    good_conduct = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    cover_letter = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    cv = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DriverApplication
        fields = ['first_name', 'surname', 'age', 'ethnicity', 'years_of_experience',
                  'kcse_certificate', 'good_conduct', 'cover_letter', 'cv']

    def clean_email(self):
        """Validate email uniqueness at the form level."""
        """Validate email uniqueness at the form level."""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different one.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.unique_id = uuid.uuid4().hex[:12]  # Generate a 12-character unique ID
        # Additional logic can be added here if needed
        if commit:
            user.save()
        return user
