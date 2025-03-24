from django.urls import path
from . import views

urlpatterns = [
    # Example view
    path('', views.index, name='index'),
]
