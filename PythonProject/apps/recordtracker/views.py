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
    this_vehicle = VehicleStats.objects.get(id = vic)
    content = {
        'vehicle' : this_vehicle,
    }
    return render(request, 'recordtracker/vehicle.html', content)


def edit(request, vic):
    this_vehicle = VehicleStats.objects.get(id = vic)
    content = {
        'vehicle' : this_vehicle,
    }
    return render(request, 'recordtracker/edit.html', content)


def update(request, vic):
    this_vehicle = VehicleStats.objects.get(id = vic)
    vehicle.make = request.POST['make']
    vehicle.model = request.POST['model']
    vehicle.year = request.POST['year']
    vehicle.odometer = request.POST['odometer']
    vehicle.logstart = request.POST['logstart']
    vehicle.oil_used = request.POST['oil_used']
    vehicle.tires = request.POST['tires']
    vehicle.notes = request.POST['notes']
    return redirect('/vehicles/'+str(this_vehicle.id))


def fuel(request, vic):
    this_vehicle = VehicleStats.objects.get(id = vic)
    fuel = VehicleFueling.objects.filter(vehicle = this_vehicle).order_by('-odometer')
    content = {
        'fuel': fuel,
        'vehicle': this_vehicle,
    }
    return render(request, 'recordtracker/vehicle_fuel.html', content)


def add_fuel(request, vic):
    this_vehicle = VehicleStats.objects.get(id = vic)
    content = {
        'vehicle': this_vehicle,
    }
    return render(request, 'recordtracker/add_fuel.html', content)


def create_fuel(request, vic):
    print(request.POST)
    this_vehicle = VehicleStats.objects.get(id = vic)
    VehicleFueling.objects.create_fuel_entry(request.POST, this_vehicle)
    return redirect('/vehicles/'+str(this_vehicle.id)+'/fuel')


def edit_fuel(request, vic, fid):
    return redirect('/')


def update_fuel(request, vic, fid):
    return redirect('/')


def delete_fuel(request, vic, fid):
    return redirect('/')


def maint(request, vic):
    return redirect('/')


def add_maint(request, vic):
    return redirect('/')


def create_maint(request, vic):
    this_vehicle = VehicleStats.objects.get(id = vic)
    return redirect('/vehicles/'+str(this_vehicle.id)+'/maint')


def edit_maint(request, vic, mid):
    return redirect('/')


def update_maint(request, vic, mid):
    return redirect('/')


def delete_maint(request, vic, mid):
    return redirect('/')
