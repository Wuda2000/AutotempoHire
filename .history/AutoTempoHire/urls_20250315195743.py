from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signupandlogin/', include('signupandlogin.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', lambda request: redirect('dashboard/')), 
 
]
