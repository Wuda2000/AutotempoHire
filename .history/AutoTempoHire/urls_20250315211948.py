from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard/')), 
    path('driver_matching/', include('driver_matching.urls')),
    path('payments/', include('payments.urls')),  
    path('reviews/', include('reviews.urls')),  
    path('tracking/', include('tracking.urls')),  
    path('auth_app/', include('auth_app.urls')),
    path('signupandlogin_django/', include('signupandlogin_django.urls')),
 
]
