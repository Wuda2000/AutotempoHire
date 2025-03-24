from django.urls import path
from . import views

urlpatterns = [
    # Example route, adjust as needed
    path('', views.index, name='driver_matching_index'),
]
