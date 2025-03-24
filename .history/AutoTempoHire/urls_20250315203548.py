from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signupandlogin/', include('signupandlogin.urls')),
    path('', lambda request: redirect('dashboard/')), 
    path('payments/', include('payments.urls')),
    path('payments/', include('payments.urls')),  # Include payments URLs
    path('reviews/', include('reviews.urls')),  # Include drivers URLs
    path('tracking/', include('tracking.urls')),  
 
]
