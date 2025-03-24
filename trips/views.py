from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from auth_app.models import Driver, CustomUser
from trips.models import Trip  
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from django.contrib import messages
from .forms import TripForm, TripUpdateForm, TripDeleteForm
from django.db.models import Q
from django.http import JsonResponse


@login_required
def trip_list(request):
    user = request.user
    driver = get_object_or_404(Driver, user=user)
    trips = Trip.objects.filter(driver=driver).order_by('-date')
    return render(request, 'driver/trip_list.html', {'trips': trips, 'driver': driver})

@login_required
def trip_create(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.driver = request.user.driver
            trip.save()
            return redirect('trip_list')
    else:
        form = TripForm()
    return render(request, 'driver/trip_create.html', {'form': form})

@login_required
def trip_update(request, trip_id):  
    trip = get_object_or_404(Trip, pk=trip_id)
    if request.method == 'POST':
        form = TripUpdateForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('trip_list')
    else:
        form = TripUpdateForm(instance=trip)
    return render(request, 'driver/trip_update.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    driver = get_object_or_404(Driver, user=user)
    trips = Trip.objects.filter(driver=driver).order_by('-date')
    return render(request, 'driver/dashboard.html', {'trips': trips, 'driver': driver})


@login_required
def driver_dashboard(request):
    pending_trips = Trip.objects.filter(car_owner=request.user, status='pending')
    completed_trips = Trip.objects.filter(car_owner=request.user, status='completed')
    return render(request, 'auth_app/dashboard.html', {
        'pending_trips': pending_trips,
        'completed_trips': completed_trips
    })


@login_required
def trip_list(request):
    user = request.user
    driver = get_object_or_404(Driver, user=user)
    trips = Trip.objects.filter(driver=driver).order_by('-date')
    return render(request, 'driver/trip_list.html', {'trips': trips, 'driver': driver})

@login_required
def car_owner_trip_list(request):
    trips = Trip.objects.filter(car_owner=request.user)
    return render(request, 'auth_app/trips/trip_list.html', {'trips': trips})

@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    return render(request, 'driver/trip_detail.html', {'trip': trip})

@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, trip_id=trip_id)  # ✅ Correct reference

    return render(request, 'auth_app/trips/trip_detail.html', {'trip': trip})


@login_required
def hire_driver(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    trip = Trip.objects.get(id=driver_id)
    trip.driver = driver
    trip.save()
    return render(request, 'auth_app/hire_driver.html', {'driver': driver})     

@login_required
def hire_driver(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    return render(request, 'auth_app/hire_driver.html', {'driver': driver})

@login_required
def hire_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)

    if request.method == "POST":
        departure_time = parse_datetime(request.POST.get('departure_time'))
        arrival_time = parse_datetime(request.POST.get('arrival_time'))
        pickup_point = request.POST.get('pickup_point')
        destination = request.POST.get('destination')
        payment_offered = request.POST.get('payment_offered')

        if not departure_time or not arrival_time:
            messages.error(request, "Please enter both departure and arrival times")
            return render(request, 'auth_app/hire_driver.html', {
                'driver': driver,
                'error': "Please enter both departure and arrival times"
            })

        if arrival_time < departure_time:
            messages.error(request, "Arrival time must be after departure time")
            return render(request, 'auth_app/hire_driver.html', {
                'driver': driver,
                'error': "Arrival time must be after departure time"
            })

        if departure_time < datetime.now():
            messages.error(request, "Departure time must be in the future")
            return render(request, 'auth_app/hire_driver.html', {
                'driver': driver,
                'error': "Departure time must be in the future"
            })

        trip = Trip.objects.create(
            car_owner=request.user,
            driver=driver.user,  
            destination=destination,
            pickup_location=pickup_point,
            trip_date=departure_time,
            price=payment_offered,
            status="pending"
        )
        trip.save()

        messages.success(request, 'Trip created successfully!')
        return redirect('trip_list')

    return render(request, 'auth_app/hire_driver.html', {'driver': driver})

       