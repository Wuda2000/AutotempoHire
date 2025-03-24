import json
from django.http import JsonResponse
from .models import Transaction  # Assuming Transaction model exists

def handle_callback(request):
    """
    Handles the callback from M-Pesa after payment processing.
    
    :param request: The HTTP request containing the callback data.
    :return: JSON response indicating success or failure.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            transaction_id = data.get("TransactionID")
            response_code = data.get("ResponseCode")

            # Update the transaction status in the database
            transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
            if transaction:
                transaction.status = "success" if response_code == "0" else "failed"
                transaction.save()

            return JsonResponse({"status": "success", "message": "Callback processed."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
