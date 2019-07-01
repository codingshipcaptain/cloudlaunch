from __future__ import unicode_literals #For models.Manager  Must be on top
from django.db import models
from django.contrib import messages
import bcrypt
import re

class VehicleStatsManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        if len(postData['FIELD']) < 2:
            errors['FIELD'] = "FIELD should be at least 2 characters"
        if len(postData['FIELD']) < 3:
            errors['FIELD'] = "FIELD should be at least 2 characters"
        if len(postData['FIELD']) < 10:
            errors['FIELD'] = "FIELD should be at least 10 characters"
        return errors

    def fuel_numbers(self, this_vehicle):
        hwy_mpg = 0
        city_mpg = 0
        off_mpg = 0
        combine_mpg = 0

        hwy_fuel = VehicleFueling.objects.filter(vehicle = this_vehicle, hwy = True, not_full = False)
        sum = 0
        if len(hwy_fuel) > 0:
            for econ in hwy_fuel:
                sum += econ.mpg
            this_vehicle.hwy_mpg = sum/len(hwy_fuel)
        else:
            this_vehicle.hwy_mpg = 0.0

        city_fuel = VehicleFueling.objects.filter(vehicle = this_vehicle, city = True, not_full = False)
        sum = 0
        if len(city_fuel) > 0:
            for econ in city_fuel:
                sum += econ.mpg
            this_vehicle.city_mpg = sum/len(city_fuel)
        else:
            this_vehicle.city_mpg = 0.0

        off_fuel = VehicleFueling.objects.filter(vehicle = this_vehicle, off = True, not_full = False)
        sum = 0
        if len(off_fuel) > 0:
            for econ in off_fuel:
                sum += econ.mpg
            this_vehicle.off_mpg = sum/len(off_fuel)
        else:
            this_vehicle.off_mpg = 0.0

        combine_fuel = VehicleFueling.objects.filter(vehicle = this_vehicle, combine = True, not_full = False)
        sum = 0
        if len(combine_fuel) > 0:
            for econ in off_fuel:
                sum += econ.mpg
            this_vehicle.combine_mpg = sum/len(combine_fuel)
        else:
            this_vehicle.combine_mpg = 0.0
        return True

    def fuel_numbers_10(self, this_vehicle):
        hwy_mpg = 0
        city_mpg = 0
        off_mpg = 0
        combine_mpg = 0
        store_h = 0
        store_c = 0
        store_o = 0
        store_cb = 0
        hwy_fuel = VehicleFueling.objects.filter(vehicle = this_vehicle, hwy = True).order_by('-odometer')[:10]
        sum = 0
        if len(hwy_fuel) > 0:
            for econ in hwy_fuel:
                sum += econ.mpg
            store_h = sum/len(hwy_fuel)
        else:
            store_h = 0.0

        city_fuel = VehicleFueling.objects.filter(vehicle = this_vehicle, city = True).order_by('-odometer')[:10]
        sum = 0
        if len(city_fuel) > 0:
            for econ in city_fuel:
                sum += econ.mpg
            store_c = sum/len(city_fuel)
        else:
            store_c = 0.0

        off_fuel = VehicleFueling.objects.filter(vehicle = this_vehicle, off = True).order_by('-odometer')[:10]
        sum = 0
        if len(off_fuel) > 0:
            for econ in off_fuel:
                sum += econ.mpg
            store_o = sum/len(off_fuel)
        else:
            store_o = 0.0

        combine_fuel = VehicleFueling.objects.filter(vehicle = this_vehicle, combine = True).order_by('-odometer')[:10]
        sum = 0
        if len(combine_fuel) > 0:
            for econ in off_fuel:
                sum += econ.mpg
            store_cb = sum/len(combine_fuel)
        else:
            store_cb = 0.0

        return {'store_h': store_h, 'store_c': store_c, 'store_o': store_o, 'store_cb': store_cb}



class VehicleStats(models.Model):
    make = models.CharField(max_length = 255)
    model = models.CharField(max_length = 100)
    year = models.IntegerField()
    odometer = models.IntegerField()
    logstart = models.DateField()
    lastoilchg = models.IntegerField(null=True, blank=True)
    oil_used = models.CharField(max_length = 100)
    hwy_mpg = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    city_mpg = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    off_mpg = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    combine_mpg = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    tires = models.CharField(max_length = 100)
    notes = models.TextField()
    trip_store = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    gallons_store = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = VehicleStatsManager()

    def __repr__(self):
        return f"<Vehicle: {self.model} ({self.id})>"


# class VehicleMaintManager(models.Manager):
#     def basic_validator(self, postData):
#         errors = {}
#         EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
#         if len(postData['FIELD']) < 2:
#             errors['FIELD'] = "FIELD should be at least 2 characters"
#         if len(postData['FIELD']) < 3:
#             errors['FIELD'] = "FIELD should be at least 2 characters"
#         if len(postData['FIELD']) < 10:
#             errors['FIELD'] = "FIELD should be at least 10 characters"
#         return errors

class VehicleFuelManager(models.Manager):
    def create_fuel_entry(self, postData, this_vehicle):
        Ehwy = False
        Ecity = False
        Eoff = False
        Ecombine = False
        if postData['driving_type'] == 'hwy':
            Ehwy = True
        elif postData['driving_type'] == 'city':
            Ecity = True
        elif postData['driving_type'] == 'off':
            Eoff = True
        else:
            Ecombine = True
        if postData['fill_type'] == 'not_full':
            VehicleFueling.objects.create(event_date = postData['event_date'], odometer = postData['odometer'],
                trip_meter = postData['trip_meter'], gallons = postData['gallons'],
                hwy = Ehwy, city = Ecity, off = Eoff, combine = Ecombine, not_full = True)
        elif postData['fill_type'] == 'now_full':
            not_fulls = VehicleFueling.objects.filter(not_full = True)
            do_combine = False
            if Ecombine == True:
                do_combine = True
            else:
                for entry in not_fulls:
                    if entry.combine == True:
                        do_combine = True
                        break
                    elif entry.hwy == True:
                        Fhwy = True
                        if Fcity == True or Foff == True:
                            do_combine = True
                            break
                    elif entry.city == True:
                        Fcity = True
                        if Fhwy == True or Foff == True:
                            do_combine = True
                            break
                    elif entry.city == True:
                        Fcity = True
                        if Fcity == True or Fhwy == True:
                            do_combine = True
                            break
            if do_combine == True:
                total_gallons = 0
                total_trip = 0
                total_gallons += float(postData['gallons'])
                total_trip += float(postData['trip_meter'])
                for entry in not_fulls:
                    total_trip += entry.trip_meter
                    total_gallons += entry.gallons
                mpg_return = total_trip / total_gallons
                for entry in not_fulls:
                    entry.hwy = False
                    entry.city = False
                    entry.off = False
                    entry.combine = True
                    entry.mpg = mpg_return
                    entry.not_full = False
                    entry.save()
                VehicleFueling.objects.create(event_date = postData['event_date'], odometer = postData['odometer'],
                    trip_meter = postData['trip_meter'], gallons = postData['gallons'],
                    hwy = False, city = False, off = False, combine = True, mpg = mpg_return, not_full = False, vehicle = this_vehicle)
            else:
                total_gallons = 0
                total_trip = 0
                total_gallons += float(postData['gallons'])
                total_trip += float(postData['trip_meter'])
                for entry in not_fulls:
                    total_trip += entry.trip_meter
                    total_gallons += entry.gallons
                mpg_return = total_trip / total_gallons
                for entry in not_fulls:
                    entry.mpg = mpg_return
                    entry.not_full = False
                    entry.save()
                VehicleFueling.objects.create(event_date = postData['event_date'], odometer = postData['odometer'],
                    trip_meter = postData['trip_meter'], gallons = postData['gallons'],
                    hwy = Ehwy, city = Ecity, off = Eoff, combine = Ecombine, not_full = postData['not_full'], vehicle = this_vehicle)
        else:
            mpg_return = float(postData['trip_meter']) / float(postData['gallons'])
            VehicleFueling.objects.create(event_date = postData['event_date'], odometer = postData['odometer'],
                trip_meter = postData['trip_meter'], gallons = postData['gallons'],
                hwy = Ehwy, city = Ecity, off = Eoff, combine = Ecombine, mpg = mpg_return, ppg = postData['ppg'], not_full = False,
                vehicle = this_vehicle)
        if int(this_vehicle.odometer) < int(postData['odometer']):
            this_vehicle.odometer = int(postData['odometer'])
            this_vehicle.save()
        return True

    def update_fuel(self, this_vehicle, fid, postData):
        update_me = VehicleFueling.objects.get(id = fid)
        Ehwy = False
        Ecity = False
        Eoff = False
        Ecombine = False
        if postData['driving_type'] == 'hwy':
            Ehwy = True
        elif postData['driving_type'] == 'city':
            Ecity = True
        elif postData['driving_type'] == 'off':
            Eoff = True
        else:
            Ecombine = True
        update_me.event_date = postData['event_date']
        update_me.odometer = postData['odometer']
        update_me.trip_meter = postData['trip_meter']
        update_me.gallons = postData['gallons']
        update_me.hwy = Ehwy
        update_me.city = Ecity
        update_me.off = Eoff
        update_me.combine = Ecombine
        update_me.mpg = postData['mpg']
        update_me.ppg = postData['ppg']
        update_me.not_full = False
        update_me.vehicle = this_vehicle
        update_me.save()
        if int(this_vehicle.odometer) < int(postData['odometer']):
            this_vehicle.odometer = int(postData['odometer'])
            this_vehicle.save()
        return True


    def delete_fuel(self, fid):
        delete_me = VehicleFueling.objects.get(id = fid)
        delete_me.delete()
        return True



class VehicleMaintManager(models.Manager):
    def create_maint_entry(self, this_vehicle, postData):
        VehicleMaint.objects.create(event_date = postData['event_date'],
            odometer = postData['odometer'], provider = postData['provider'],
            maint= postData['maint'], is_oilchg = postData['is_oilchg'],
             vehicle = this_vehicle)
        if int(this_vehicle.odometer) < int(postData['odometer']):
            this_vehicle.odometer = int(postData['odometer'])
            this_vehicle.save()
        if postData['is_oilchg'] == True and int(postData['odometer']) > int(this_vehicle.lastoilchg):
            this_vehicle.lastoilchg = postData['odometer']
            this_vehicle.oil_used = postData['oil_used']
            this_vehicle.save()
        if 'new_tire' in postData:
            this_vehicle.tires = postData['new_tire']

    def update_maint(self, this_vehicle, mid, postData):
        print(this_vehicle.odometer)
        update_me = VehicleMaint.objects.get(id = mid)
        update_me.event_date = postData['event_date']
        update_me.odometer = postData['odometer']
        update_me.provider = postData['provider']
        update_me.maint = postData['maint']
        update_me.is_oilchg = postData['is_oilchg']
        update_me.oil_used = postData['oil_used']
        update_me.vehicle = this_vehicle
        update_me.save()
        if int(this_vehicle.odometer) < int(postData['odometer']):
            this_vehicle.odometer = int(postData['odometer'])
            this_vehicle.save()
        if postData['is_oilchg'] == 'True' and (this_vehicle.lastoilchg == None or int(this_vehicle.lastoilchg) <= int(postData['odometer'])):
            this_vehicle.lastoilchg = int(postData['odometer'])
            this_vehicle.save()
        return True


    def delete_maint(self, mid):
        delete_me = VehicleMaint.objects.get(id = mid)
        delete_me.delete()
        return True


class VehicleMaint(models.Model):
    event_date = models.DateField()
    odometer = models.IntegerField()
    provider = models.CharField(max_length = 255)
    maint = models.TextField()
    is_oilchg = models.BooleanField()
    oil_used = models.CharField(max_length = 255, null=True, blank=True)
    vehicle = models.ForeignKey(VehicleStats, related_name='records', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = VehicleMaintManager()

    def __repr__(self):
        return f"<Maintenance Event Date: {self.event_date} ({self.id})>"


class VehicleFueling(models.Model):
    event_date = models.DateField()
    odometer = models.IntegerField()
    trip_meter = models.DecimalField(max_digits=4, decimal_places=1)
    gallons = models.DecimalField(max_digits=5, decimal_places=3)
    hwy = models.BooleanField()
    city = models.BooleanField()
    off = models.BooleanField()
    combine = models.BooleanField()
    mpg = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=False)
    ppg = models.DecimalField(max_digits=4, decimal_places=3)
    not_full = models.BooleanField()
    vehicle = models.ForeignKey(VehicleStats, related_name='fuel_records', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = VehicleFuelManager()

    def __repr__(self):
        return f"<Fill Up Date: {self.event_date} (Own ID: {self.id}, Veh ID: {self.vehicle})>"
