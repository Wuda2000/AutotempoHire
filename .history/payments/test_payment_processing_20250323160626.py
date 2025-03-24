import os
import unittest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.conf import settings

# Set up Django settings for testing
os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project_name.settings'  # Replace with your actual project name
import django
django.setup()

class ProcessPaymentViewTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_process_payment_success(self):
        response = self.client.post(reverse('process_payment'), {
            'phone_number': '1234567890',
            'amount': 100.0
        })
        self.assertEqual(response.status_code, 200)
        # Add assertions to check the response content for successful payment

    def test_process_payment_missing_fields(self):
        response = self.client.post(reverse('process_payment'), {
            'phone_number': '',
            'amount': 100.0
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Phone number and amount are required.")

    def test_process_payment_invalid_amount(self):
        response = self.client.post(reverse('process_payment'), {
            'phone_number': '1234567890',
            'amount': 'invalid_amount'
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Invalid amount format.")

if __name__ == "__main__":
    unittest.main()
