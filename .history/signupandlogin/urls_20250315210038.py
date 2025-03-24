from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your view paths here
    path('', views.index, name='index'),  # Example
]
