from payments.at_auth import get_access_token  # Ensure this module correctly fetches M-Pesa access token

from payments.payment_module import MpesaPayment
from payments.models import Transaction  # Assuming Transaction model exists
import logging

# Configure logging
logger = logging.getLogger(__name__)

def initiate_payment(phone_number, amount, transaction_id):
    """
    Initiates a payment request to M-Pesa.
    
    :param phone_number: The recipient's phone number (should be in international format, e.g., 2547XXXXXXXX)
    :param amount: The amount to be paid (float or int)
    :return: M-Pesa API response or error message
    """
    try:
        mpesa = MpesaPayment()  # Instantiate the MpesaPayment class
        response = mpesa.initiate_payment(
            phone_number=phone_number,  # User-provided phone number
            amount=amount,  # Validated amount
            callback_url="https://62bd-2c0f-6300-d0b-c800-89ee-637-48ac-ec9e.ngrok-free.app/driver_hiring_system/payments/callback/"
        )


        logger.info("Payment Initiated: %s", response)

        # Handle different response statuses
        if response.get("ResponseCode") == "0":
            return {"status": "success", "message": "Payment initiated successfully."}
        elif response.get("ResponseCode") in ["1", "2"]:
            return {"status": "pending", "message": "Payment is pending. Please check back later."}
        else:
            return {"status": "error", "message": "Payment failed. Please try again."}

        # Record the transaction in the database immediately after initiation
        transaction = Transaction(user=None, driver=None, amount=amount, status="pending")
        transaction.save()



    except Exception as e:
        logger.error("Payment Error: %s", str(e))
        return {"error": str(e)}

# Example Usage (for testing)
if __name__ == "__main__":
    phone_number = input("Enter phone number (e.g., 254712345678): ")
    
    try:
        amount = float(input("Enter payment amount: "))
        response = initiate_payment(phone_number, amount)
        print("Payment Response:", response)
    except ValueError:
        print("Invalid amount! Please enter a numeric value.")
