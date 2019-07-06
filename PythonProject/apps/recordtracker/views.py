from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages #for messages
from .models import * #For adding in models, * captures all
import decimal

def index(request):
    return render(request, 'recordtracker/index.html')


def main(request):
    vehicles = VehicleStats.objects.all()
    for vehicle in vehicles:
        VehicleStats.objects.fuel_numbers(vehicle)
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
    VehicleStats.objects.fuel_numbers(this_vehicle)
    mpg_nums = VehicleStats.objects.fuel_numbers_10(this_vehicle)
    diff_from_life = {
        'h_diff': decimal.Decimal(mpg_nums['store_h']) - decimal.Decimal(this_vehicle.hwy_mpg),
        'c_diff': decimal.Decimal(mpg_nums['store_c']) - decimal.Decimal(this_vehicle.city_mpg),
        'o_diff': decimal.Decimal(mpg_nums['store_o']) - decimal.Decimal(this_vehicle.off_mpg),
        'cb_diff': decimal.Decimal(mpg_nums['store_cb']) - decimal.Decimal(this_vehicle.combine_mpg),
    }
    miles_to_oilchg = this_vehicle.lastoilchg + 10000 - this_vehicle.odometer
    content = {
        'vehicle' : this_vehicle,
        'mpg_nums' : mpg_nums,
        'miles_to_oilchg': miles_to_oilchg,
        'diff_from_life': diff_from_life
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
    this_vehicle = VehicleStats.objects.get(id = vic)
    this_fuel = VehicleFueling.objects.get(id = fid)
    content = {
        'this_fuel': this_fuel,
        'vehicle': this_vehicle
    }
    return render(request, 'recordtracker/edit_fuel.html', content)


def update_fuel(request, vic, fid):
    this_vehicle = VehicleStats.objects.get(id = vic)
    VehicleFueling.objects.update_fuel(vic, fid, request.POST)
    return redirect('/vehicles/'+str(this_vehicle.id)+'/fuel')


def delete_fuel(request, vic, fid):
    this_vehicle = VehicleStats.objects.get(id = vic)
    VehicleFueling.objects.delete_fuel(fid)
    return redirect('/vehicles/'+str(this_vehicle.id)+'/fuel')


def maint(request, vic):
    this_vehicle = VehicleStats.objects.get(id = vic)
    maint = VehicleMaint.objects.filter(vehicle = this_vehicle).order_by('-odometer')
    content = {
        'maint' : maint,
        'vehicle' : this_vehicle
    }
    return render(request, 'recordtracker/vehicle_maint.html', content)


def add_maint(request, vic):
    this_vehicle = VehicleStats.objects.get(id = vic)
    content = {
        'vehicle' : this_vehicle
    }
    return render(request, 'recordtracker/add_maint.html', content)


def create_maint(request, vic):
    this_vehicle = VehicleStats.objects.get(id = vic)
    VehicleMaint.objects.create_maint_entry(this_vehicle, request.POST)
    return redirect('/vehicles/'+str(this_vehicle.id)+'/maint')


def edit_maint(request, vic, mid):
    this_vehicle = VehicleStats.objects.get(id = vic)
    this_maint = VehicleMaint.objects.get(id = mid)
    content = {
        'this_maint': this_maint,
        'vehicle': this_vehicle
    }
    return render(request, 'recordtracker/edit_maint.html', content)


def update_maint(request, vic, mid):
    this_vehicle = VehicleStats.objects.get(id = vic)
    VehicleMaint.objects.update_maint(this_vehicle, mid, request.POST)
    return redirect('/vehicles/'+str(this_vehicle.id)+'/maint')


def delete_maint(request, vic, mid):
    this_vehicle = VehicleStats.objects.get(id = vic)
    VehicleMaint.objects.delete_maint(mid)
    return redirect('/vehicles/'+str(this_vehicle.id)+'/maint')

def search_maint(request, vic):
    return redirect('/vehicles/'+str(vic)+'/maint/result/' + str(request.POST['search']))

def search_result(request, vic, search):
    this_vehicle = VehicleStats.objects.get(id = vic)
    maint = VehicleMaint.objects.search_maint(this_vehicle, search).order_by('-odometer')
    content = {
        'maint' : maint,
        'vehicle' : this_vehicle
    }
    return render(request, 'recordtracker/vehicle_maint.html', content)
