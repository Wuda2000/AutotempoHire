from django.contrib import admin
from django.urls import path, include
from tracking.urls import urlpatterns as tracking_urls  # Include tracking URLs
from auth_app import views
from django.shortcuts import redirect

urlpatterns = [
    path('auth/', include('auth_app.urls')),  
    path('', views.home, name='home'),
    path('driver_matching/', include('driver_matching.urls')),
    path('payments/', include('payments.urls')),  
    path('reviews/', include('reviews.urls')),  
    path('tracking/', include(tracking_urls)),  
    path('auth_app/', include('auth_app.urls')),
    path('signupandlogin_django/', include('signupandlogin_django.urls')),
]
