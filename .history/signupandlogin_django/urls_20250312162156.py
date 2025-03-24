from django.contrib import admin
from django.urls import path, include
from auth_app.views import home  # ✅ Import the home view

urlpatterns = [
    path('', home, name='home'),  # ✅ This will now serve home.html
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),  
]
