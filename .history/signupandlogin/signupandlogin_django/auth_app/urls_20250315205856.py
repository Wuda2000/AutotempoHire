from django.urls import path 

from .views import (
    register, 
    ApiLoginView, 
    api_register, 
    dashboard, 
    home, 
    login_view, 
    forgot_password,  
    reset_password,
    profile,
    logout_view,
    driver_list_view,
    verify_email,
    driver_profile_view,
    
)

urlpatterns = [
    path('', home, name='home'),  
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', reset_password, name='reset_password'),
    path('api/register/', api_register, name='api_register'),
    path('api/login/', ApiLoginView.as_view(), name='api_login'),

    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),


    path('profile/', profile, name='profile'),  
    path('verify/<str:token>/', verify_email, name='verify_email'),
    path('drivers/', driver_list_view, name='driver_list'), 

]
