import requests
import base64
from datetime import datetime
from requests.auth import HTTPBasicAuth
import logging
import os
import re  # Ensure re is imported for validation

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class MpesaPayment:
    def __init__(self):
        # Load environment variables
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY")
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
        self.shortcode = os.getenv("MPESA_SHORTCODE")
        self.passkey = os.getenv("MPESA_PASSKEY")

        # Ensure all required credentials are set
        if not all([self.consumer_key, self.consumer_secret, self.shortcode, self.passkey]):
            logger.error("Missing one or more MPESA environment variables.")
            raise ValueError("Ensure MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET, MPESA_SHORTCODE, and MPESA_PASSKEY are set in the .env file.")

        self.base_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    def get_access_token(self):
        """
        Fetches an access token from Safaricom's API.
        """
        try:
            response = requests.get(
                self.base_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret)
            )
            response.raise_for_status()  # Raise an error if request fails
            return response.json().get("access_token")
        except requests.RequestException as e:
            logger.error(f"Error fetching access token: {e}")
            return None

    def generate_password(self):
        """
        Generates the base64-encoded password for STK Push authentication.
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return base64.b64encode(data_to_encode.encode()).decode(), timestamp

def initiate_payment(self, phone_number, amount, callback_url, transaction_id):

        """
        Initiates an M-Pesa STK Push request.

        :param phone_number: The phone number making the payment.
        :param amount: The amount to be paid.
        :param callback_url: The URL where M-Pesa will send the payment confirmation.
        :return: JSON response from M-Pesa API.
        """
        access_token = self.get_access_token()
        if not access_token:
            return {"error": "Failed to retrieve access token"}

        password, timestamp = self.generate_password()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        # Validate user payment details
        if not self.validate_payment_details(phone_number, amount):
            return {"error": "Invalid payment details"}

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
            "CallBackURL": callback_url,
            "AccountReference": "AutoTempoHire",
            "TransactionDesc": "Driver hiring payment",
            "TransactionID": transaction_id

        }

        try:
            response = requests.post(self.stk_url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for failed requests
            response_data = response.json()

            # Log response for debugging
            logger.info(f"STK Push Response: {response_data}")

            return response_data
        except requests.RequestException as e:
            logger.error(f"STK Push request failed: {e}")
            return {"error": str(e)}


def is_duplicate_transaction(self, transaction_id):
    """Check if the transaction ID already exists."""
    # Logic to check for duplicate transaction IDs
    existing_transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
    return existing_transaction is not None


def validate_payment_details(self, phone_number, amount):
    """Validate user payment details before processing."""
    if not isinstance(amount, (int, float)) or amount <= 0:
        return False
    if not re.match(r"^\+?254\d{9}$", phone_number):  # Validate Kenyan phone number format
        return False
    return True


def process_payment(user, driver, amount, callback_url, transaction_id, retry_count=0):

    # Record the transaction in the database immediately after initiation
    transaction = Transaction(user=user, driver=driver, amount=amount, transaction_id=transaction_id, status="pending")

    transaction.save()


    """
    Handles the payment process when hiring a driver.

    :param user: The user making the payment (CarOwner).
    :param driver: The driver being hired.
    :param amount: The amount to be paid.
    :param callback_url: The callback URL for M-Pesa.
    :return: Success or error message.
    """
    mpesa = MpesaPayment()
    response = mpesa.initiate_payment(user.phone_number, amount, callback_url, transaction_id)

    # Check for failed transactions and retry if necessary
    if response.get("ResponseCode") != "0" and retry_count < 3:
        logger.warning(f"Payment failed for transaction {transaction_id}. Retrying...")
        return self.process_payment(user, driver, amount, callback_url, transaction_id, retry_count + 1)



    # M-Pesa success response usually contains 'ResponseCode': '0'
    if response.get("ResponseCode") == "0":
        driver.available = False
        driver.save()
        return {"status": "success", "message": "Payment successful. Driver hired."}
    else:
        return {"status": "error", "message": response.get("error", "Payment failed. Try again.")}


# Example usage (for debugging)
if __name__ == "__main__":
    test_phone = "2547XXXXXXXX"  # Replace with a valid Safaricom number
    test_amount = 500  # Example amount
    test_callback_url = "https://yourdomain.com/mpesa/callback/"

    payment_response = MpesaPayment().initiate_payment(test_phone, test_amount, test_callback_url)
    print(payment_response)
