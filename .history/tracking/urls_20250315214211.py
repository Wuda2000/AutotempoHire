from django.urls import path
from .views import tracking_view  # Import the view to be created

urlpatterns = [
    path('', tracking_view, name='tracking_index'),  # Define the URL pattern for the tracking view
]
