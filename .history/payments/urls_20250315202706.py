from django.urls import path
from .views import initiate_payment, mpesa_callback

urlpatterns = [
    path('pay/', initiate_payment, name='initiate_payment'),
    path('callback/', mpesa_callback, name='mpesa_callback'),
]