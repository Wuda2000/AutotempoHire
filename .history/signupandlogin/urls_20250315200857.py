from django.urls import path
from .views import 

urlpatterns = [
    path('', dashboard_view, name='dashboard_home'),
    path('drivers/', driver_list_view, name='driver_list'),  # This links to driver_list.html
]
