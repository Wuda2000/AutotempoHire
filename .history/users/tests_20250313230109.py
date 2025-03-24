from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class UserTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'testuser@example.com'
        self.user = get_user_model().objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'role': 'car_owner'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful signup
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())  # Check if user was created

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful login
        self.assertEqual(response.wsgi_request.user, self.user)  # Check if user is authenticated
