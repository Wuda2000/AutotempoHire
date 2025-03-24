from django.test import TestCase
from .forms import CustomUserCreationForm, DriverApplicationForm
from .models import CustomUser, DriverApplication

class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'role': 'driver',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        CustomUser.objects.create(username='existinguser', email='test@example.com', password='password123')
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'role': 'driver',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('This email is already registered. Please use a different one.', form.errors['email'])

class DriverApplicationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'surname': 'Doe',
            'age': 25,
            'ethnicity': 'Kikuyu',
            'years_of_experience': 2,
            'kcse_certificate': 'path/to/kcse_certificate.pdf',
            'good_conduct': 'path/to/good_conduct.pdf',
            'cover_letter': 'path/to/cover_letter.pdf',
            'cv': 'path/to/cv.pdf',
        }
        form = DriverApplicationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_age_validation(self):
        form_data = {
            'first_name': 'John',
            'surname': 'Doe',
            'age': 20,
            'ethnicity': 'Kikuyu',
            'years_of_experience': 2,
            'kcse_certificate': 'path/to/kcse_certificate.pdf',
            'good_conduct': 'path/to/good_conduct.pdf',
            'cover_letter': 'path/to/cover_letter.pdf',
            'cv': 'path/to/cv.pdf',
        }
        form = DriverApplicationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("You must be at least 21 years old to apply.", form.errors['age'])
