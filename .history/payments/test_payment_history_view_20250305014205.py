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

class PaymentHistoryViewTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_payment_history_view(self):
        response = self.client.get(reverse('payment_history'))  # Fetch the payment history view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/payment_history.html')
        self.assertContains(response, "Your Payment History")  # Check for specific content

    def test_payment_history_empty(self):
        # Assuming the user has no payment history
        response = self.client.get(reverse('payment_history'))  # Fetch the payment history view
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No payment history available.")  # Check for message when no history

if __name__ == "__main__":
    unittest.main()
