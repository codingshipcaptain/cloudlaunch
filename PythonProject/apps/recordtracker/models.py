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
    mpg = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=False)
    ppg = models.DecimalField(max_digits=4, decimal_places=3)
    not_full = models.BooleanField()
    vehicle = models.ForeignKey(VehicleStats, related_name='fuel_records', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # objects = NAMEManager()

    def __repr__(self):
        return f"<Fill Up Date: {self.event_date} ({self.id})>"
