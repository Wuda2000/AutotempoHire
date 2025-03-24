from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from payments.mpesa_api import MpesaGateway

@csrf_exempt
def process_payment(request):
    """Handles M-Pesa payment requests."""
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        amount = request.POST.get("amount")

        if not phone_number or not amount:
            return JsonResponse({"error": "Phone number and amount are required."}, status=400)

        try:
            amount = float(amount)  # Ensure amount is numeric
            mpesa_gateway = MpesaGateway()
            payment_response = mpesa_gateway.initiate_payment(phone_number, amount)
            return JsonResponse(payment_response)
        except ValueError:
            return JsonResponse({"error": "Invalid amount format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
