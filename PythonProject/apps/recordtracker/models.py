from __future__ import unicode_literals #For models.Manager  Must be on top
from django.db import models
from django.contrib import messages
import bcrypt
import re

# class VehicleStatsManager(models.Manager):
    # def basic_validator(self, postData):
    #     errors = {}
    #     EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
    #     if len(postData['FIELD']) < 2:
    #         errors['FIELD'] = "FIELD should be at least 2 characters"
    #     if len(postData['FIELD']) < 3:
    #         errors['FIELD'] = "FIELD should be at least 2 characters"
    #     if len(postData['FIELD']) < 10:
    #         errors['FIELD'] = "FIELD should be at least 10 characters"
    #     return errors


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
    # objects = VehicleStatsManager()

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
                hwy = Ehwy, city = Ecity, off = Eoff, combine = Ecombine, not_full = postData['not_full'])
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
                hwy = Ehwy, city = Ecity, off = Eoff, combine = Ecombine, mpg = mpg_return, ppg = postData['ppg'], not_full = False, vehicle = this_vehicle)
        this_vehicle.odometer = postData['odometer']
        this_vehicle.save()


class VehicleMaint(models.Model):
    event_date = models.DateField()
    odometer = models.IntegerField()
    provider = models.CharField(max_length = 255)
    maint = models.TextField()
    is_oilchg = models.BooleanField()
    vehicle = models.ForeignKey(VehicleStats, related_name='records', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # objects = VehicleMaintManager()

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
