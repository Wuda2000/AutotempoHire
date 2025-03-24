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
