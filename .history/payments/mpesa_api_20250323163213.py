import requests
import base64
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os

import logging

class MpesaGateway:
    # Configure logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


    def __init__(self):
        """Initialize M-Pesa API credentials from environment variables."""
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY")
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
        self.shortcode = os.getenv("MPESA_SHORTCODE")
        self.passkey = os.getenv("MPESA_PASSKEY")
        self.callback_url = os.getenv("MPESA_CALLBACK_URL")
        self.token_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # Production URL
        self.stk_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # Production URL
        self.sandbox_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # Sandbox URL
        self.sandbox_stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # Sandbox URL

    def get_access_token(self):
        """Retrieves M-Pesa API access token."""
        try:
            response = requests.get(
                self.token_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret)
            )
            response.raise_for_status()
            return response.json().get("access_token")
        except requests.RequestException as e:
            return {"error": f"Failed to fetch access token: {str(e)}"}

    def generate_password(self):
        """Generates password and timestamp for STK push request."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        data_to_encode = f"{self.shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(data_to_encode.encode()).decode()
        return password, timestamp

    def is_token_expired(self, token):
        """Check if the access token is expired."""
        # Logic to determine if the token is expired
        return False  # Placeholder for actual expiration check

    def refresh_access_token(self):
        """Refresh the access token."""
        try:
            response = requests.get(
                self.token_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret)
            )
            response.raise_for_status()
            return response.json().get("access_token")
        except requests.RequestException as e:
            return {"error": f"Failed to refresh access token: {str(e)}"}

    def initiate_payment(self, phone_number, amount, transaction_id):

        """Initiates a payment request using M-Pesa STK push."""
        access_token = self.get_access_token()  # Get access token
        if not access_token or "error" in access_token:
            return {"error": "Failed to get access token"}
        # Check if token is expired and refresh if necessary
        if self.is_token_expired(access_token):
            access_token = self.refresh_access_token()

        if not access_token or "error" in access_token:
            return {"error": "Failed to get access token"}

        password, timestamp = self.generate_password()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Check for duplicate transaction
        if self.is_duplicate_transaction(transaction_id):
            return {"error": "Duplicate transaction"}

        payload = {

            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": "AutoTempoHire",
            "TransactionDesc": "Payment for driver hire"
            "TransactionID": transaction_id
        }


        try:
            response = requests.post(self.stk_url, headers=headers, json=payload, timeout=10)  # Set timeout

            response.raise_for_status()
            response_data = response.json()
            if response.status_code != 200:
                return {"error": "Payment request failed", "details": response_data}
            return response_data

        except requests.RequestException as e:
            self.logger.error(f"Payment request failed: {str(e)}")

            return {"error": f"Payment request failed: {str(e)}"}
