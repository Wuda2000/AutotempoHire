from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthAppTests(TestCase):

    def setUp(self):
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
            'role': 'carOwner'
        }
        self.invalid_user_data = {
            'username': '',
            'email': 'invalidemail',
            'password1': 'short',
            'password2': 'short'
        }
        self.user = User.objects.create_user(username='existinguser', email='existing@example.com', password='password123')

    def test_api_register_valid_data(self):
        response = self.client.post(reverse('api_register'), self.valid_user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully.', response.json().get('message'))

    def test_api_register_invalid_data(self):
        response = self.client.post(reverse('api_register'), self.invalid_user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.json().get('error'))

    def test_api_register_duplicate_email(self):
        self.valid_user_data['email'] = 'existing@example.com'
        response = self.client.post(reverse('api_register'), self.valid_user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('This email is already registered.', response.json().get('error'))

    def test_register_form(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_app/register.html')

        response = self.client.post(reverse('register'), self.valid_user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Registration successful.', response.json().get('message'))

    def test_register_form_invalid(self):
        response = self.client.post(reverse('register'), self.invalid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('This field is required.', response.context['form'].errors['username'])

    def test_become_driver_form(self):
        self.client.login(username='testuser', password='StrongPassword123!')
        response = self.client.get(reverse('become_driver'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_app/become_driver.html')

        # Add more tests for valid and invalid submissions as needed

# Additional tests for CSRF protection and authentication flows can be added here.
