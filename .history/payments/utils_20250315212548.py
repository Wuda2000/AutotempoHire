from django.http import JsonResponse
from payments.mpesa_api import MpesaGateway

def process_payment(phone_number, amount):
    """Processes the payment using M-Pesa."""
    try:
        mpesa_gateway = MpesaGateway()
        payment_response = mpesa_gateway.initiate_payment(phone_number, amount)
        return payment_response
    except Exception as e:
        return {"error": str(e)}
