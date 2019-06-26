from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages #for messages
from .models import * #For adding in models, * captures all

def index(request):
    return render(request, 'recordtracker/index.html')


def main(request):
    vehicles = VehicleStats.objects.all()
    content = {
        'vehicle_list': vehicles,
    }

    return render(request, 'recordtracker/main.html', content)


def new(request):
    return render(request, 'recordtracker/new.html')


def create(request):
    VehicleStats.objects.create(make = request.POST['make'], model = request.POST['model'], year = request.POST['year'], odometer = request.POST['odometer'], logstart=request.POST['logstart'], oil_used = request.POST['oil_used'], tires = request.POST['tires'], notes = request.POST['notes'])
    return redirect('/')


def show(request, vic):
    vehicle = VehicleStats.objects.get(id = vic)
    content = {
        'vehicle' : vehicle,
    }
    return render(request, 'recordtracker/vehicle.html', content)


def edit(request, vic):
    vehicle = VehicleStats.objects.get(id = vic)
    content = {
        'vehicle' : vehicle,
    }
    return render(request, 'recordtracker/edit.html', content)

def update(request, vic):
    vehicle = VehicleStats.objects.get(id = vic)
    vehicle.make = request.POST['make']
    vehicle.model = request.POST['model']
    vehicle.year = request.POST['year']
    vehicle.odometer = request.POST['odometer']
    vehicle.logstart = request.POST['logstart']
    vehicle.oil_used = request.POST['oil_used']
    vehicle.tires = request.POST['tires']
    vehicle.notes = request.POST['notes']
    return redirect('/vehicles/'+str(vehicle.id))

def fuel():
    return redirect('/')
def add_fuel():
    return redirect('/')
def edit_fuel():
    return redirect('/')
def update_fuel():
    return redirect('/')
def delete_fuel():
    return redirect('/')
def maint():
    return redirect('/')
def add_maint():
    return redirect('/')
def edit_maint():
    return redirect('/')
def update_maint():
    return redirect('/')
def delete_maint():
    return redirect('/')
