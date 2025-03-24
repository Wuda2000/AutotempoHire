from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .payment_module import stk_push
import json

def initiate_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone_number = data.get("phone_number")
        amount = data.get("amount")
        
        if not phone_number or not amount:
            return JsonResponse({"error": "Phone number and amount are required"}, status=400)
        
        response = stk_push(phone_number, amount)
        return JsonResponse(response)

@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("M-Pesa Callback Data:", data)  # Log the response for debugging
        return JsonResponse({"message": "Callback received"})