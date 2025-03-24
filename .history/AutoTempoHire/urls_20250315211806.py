from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signupandlogin/', include('signupandlogin.urls')),
    path('', lambda request: redirect('dashboard/')), 
    path('driver_matching/', include('driver_matching.urls')),
    path('payments/', include('payments.urls')),  
    path('reviews/', include('reviews.urls')),  
    path('tracking/', include('tracking.urls')),  
    path('a/', include('signupandlogin.urls')),
 
]
