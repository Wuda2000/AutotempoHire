from django.shortcuts import render, redirect
from .forms import DriverForm, CarOwnerForm
from .models import DriverProfile

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

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

