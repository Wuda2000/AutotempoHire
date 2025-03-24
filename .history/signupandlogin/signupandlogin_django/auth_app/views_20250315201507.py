import json 
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.utils.crypto import get_random_string  
from django.urls import reverse  
from django.contrib.auth.models import Group  
from django.contrib.auth.password_validation import validate_password  
from django.core.exceptions import ValidationError
from rest_framework.views import APIView  
from .forms import CustomUserCreationForm, DriverForm, CarOwnerForm
from .models import CustomUser,
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import
from .models import 



@login_required
def dashboard(request):
    return render(request, 'auth_app/dashboard.html', {'user': request.user})

def home(request):
    return render(request, 'auth_app/home.html')

@login_required
def profile(request):
    return render(request, 'auth_app/profile.html', {'user': request.user})


def verify_email(request, token):
    """Verify the user's email when they click the email link."""
    try:
        user = CustomUser.objects.get(password_reset_token=token)
        user.is_active = True
        user.password_reset_token = None  # Clear the token after verification
        user.save()
        return redirect('home')  # ✅ Redirect to home page after verification
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Invalid verification token.'}, status=400)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.filter(email=email).first()  

            if not user:
                return JsonResponse({'error': 'Email not found.'}, status=400)

            reset_token = get_random_string(length=32)
            user.password_reset_token = reset_token
            user.save()

            reset_link = request.build_absolute_uri(reverse('reset_password', args=[reset_token]))
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'noreply@autotempohire.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Password reset link sent to your email.'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    return render(request, 'auth_app/forgot_password.html')

def reset_password(request, token):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)

        try:
            validate_password(new_password)  

            user = CustomUser.objects.get(password_reset_token=token)
            user.set_password(new_password)
            user.password_reset_token = None  
            user.save()
            return JsonResponse({'message': 'Password reset successful. Please login with your new password.'}, status=200)

        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)  

        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Invalid token.'}, status=400)

    return render(request, 'auth_app/reset_password.html', {'token': token})


@csrf_exempt
def api_register(request):    
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password1')
        confirm_password = data.get('password2')
        role = data.get('role')

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'error': 'This email is already registered. Please use a different one.'}, status=400)

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)

        try:
            validate_password(password)  

            user = CustomUser.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                role=role
            )

            group = Group.objects.get_or_create(name='CarOwners' if role == 'carOwner' else 'Drivers')[0]
            user.groups.add(group)

            return JsonResponse({'message': 'User registered successfully.'}, status=201)

        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)  

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


class ApiLoginView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        

def send_verification_email(user):
    """Send an email verification link after user registration."""
    verification_token = get_random_string(length=32)
    user.password_reset_token = verification_token  # Store token for verification
    user.save()

    verification_link = f"http://127.0.0.1:8000/auth/verify/{verification_token}/"

    send_mail(
        'Verify Your Email - AutoTempoHire',
        f'Hello {user.username},\n\nClick the link below to verify your email:\n{verification_link}',
        'fridawawuda@gmail.com',  # ✅ Updated sender email
        [user.email],
        fail_silently=False,
    )


def register(request):    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Prevent login until email is verified
            user.save()

            send_verification_email(user)  # ✅ Send verification email

            return JsonResponse({'message': 'Registration successful. Check your email to verify your account.'}, status=201)

    else:
        form = CustomUserCreationForm()

    return render(request, 'auth_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            return render(request, 'auth_app/login.html', {'error': 'Invalid credentials'})

    return render(request, 'auth_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def role_selection_view(request):
    if request.method == 'POST':
        if request.user.role == 'driver':
            form = DriverForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
        elif request.user.role == 'car_owner':
            form = CarOwnerForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
        return redirect('dashboard')
    else:
        form = DriverForm() if request.user.role == 'driver' else CarOwnerForm()
    return render(request, 'dashboard/role_selection.html', {'form': form})



def driver_list_view(request):
    drivers = DriverProfile.objects.filter(verified=True)
    return render(request, 'dashboard/driver_list.html', {'drivers': drivers})


