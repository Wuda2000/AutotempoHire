from django.contrib import admin
from django.urls import path, include
from auth_app.views import home  

urlpatterns = [
    path('', home, name='home'),  
    
    path('auth/', include('auth_app.urls')),  
]
