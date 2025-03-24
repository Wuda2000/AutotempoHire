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
