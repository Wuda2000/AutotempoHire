import requests
import json
import os
from dotenv import load_dotenv
from payments.at_auth import get_access_token  # Import the authentication function

# Load environment variables
load_dotenv()

# Safaricom API Credentials
CONSUMER_KEY = os.getenv("SAFARICOM_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("SAFARICOM_CONSUMER_SECRET")
SHORTCODE = os.getenv("SAFARICOM_SHORTCODE")  # Your business SMS shortcode

def get_access_token():
    """
    Generates OAuth access token for Safaricom API.
    
    :return: Access token as a string or None if request fails.
    """
    url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
        response.raise_for_status()  # Raise HTTP errors (4xx, 5xx)
        return response.json().get("access_token")
    except requests.RequestException as e:
        print(f"Error obtaining access token: {e}")
        return None

def send_sms(phone_number, message):
    """
    Sends SMS using Safaricom Business SMS API.
    
    :param phone_number: Recipient phone number (e.g., 2547XXXXXXXX)
    :param message: Message text to send
    :return: JSON response or error message
    """
    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to get access token"}

    url = "https://api.safaricom.co.ke/mpesa/sms/v1/send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "shortCode": SHORTCODE,
        "to": phone_number,
        "message": message
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Ensure we catch HTTP errors
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    phone_number = input("Enter phone number (e.g., 2547XXXXXXXX): ")
    message = "Please enter your M-Pesa PIN to complete the payment."
    
    response = send_sms(phone_number, message)
    print(response)
