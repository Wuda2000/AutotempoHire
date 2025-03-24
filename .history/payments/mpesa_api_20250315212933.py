import requests
import base64
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os

class MpesaGateway:
    def __init__(self):
        """Initialize M-Pesa API credentials from environment variables."""
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY")
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
        self.shortcode = os.getenv("MPESA_SHORTCODE")
        self.passkey = os.getenv("MPESA_PASSKEY")
        self.callback_url = os.getenv("MPESA_CALLBACK_URL")
        self.token_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.stk_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

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

    def initiate_payment(self, phone_number, amount):
        """Initiates a payment request using M-Pesa STK push."""
        access_token = self.get_access_token()
        if not access_token or "error" in access_token:
            return {"error": "Failed to get access token"}

        password, timestamp = self.generate_password()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

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
        }

        try:
            response = requests.post(self.stk_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Payment request failed: {str(e)}"}
