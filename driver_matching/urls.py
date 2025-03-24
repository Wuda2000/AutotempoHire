from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='driver_matching_index'),
]
