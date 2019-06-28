from __future__ import unicode_literals #For models.Manager  Must be on top
from django.db import models
from django.contrib import messages
from datetime import datetime
import bcrypt
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Please check and enter a valid email.'
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['match'] = 'That email is in use. Try logging in.'
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters."
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last Name should be at least 2 characters."
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 10 characters."
        if postData['password'] != postData['cpassword']:
            errors['passmatch'] = 'Password entries do not match.'
        return errors
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Please check and enter a valid email.'
        if len(User.objects.filter(email = postData['email'])) == 0:
            errors['match'] = 'No such email.'
        if len(postData['password']) < 8:
            errors['password'] = "Password sucks bro"
        return errors
    def return_user(self, postData):
        result = User.objects.get(email = postData['email'])
        return result
    def return_user_on_uid(self, uid):
        result = User.objects.get(id = uid)
        return result

class WishManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['wish']) < 3:
            errors['wish'] = "Wish should be at least 3 characters."
        if len(postData['desc']) < 3:
            errors['desc'] = "Description should be at least 3 characters."
        return errors

    def get_wishes(self, uid):
        user_id = User.objects.get(id=uid)
        wishes = Wish.objects.filter(created_by = user_id, granted = False)
        return wishes

    def get_granted(self):
        granted = Wish.objects.filter(granted = True)
        return granted

    def wish_granted(self, wid):
        update_me = Wish.objects.get(id = wid)
        update_me.granted = True
        update_me.granted_date = datetime.now()
        update_me.save()
        return True

    def like_wish(self, uid, wid):
        user_id = User.objects.get(id=uid)
        like_me = Wish.objects.get(id = wid)
        like_me.liked_by.add(user_id)
        like_me.likes += 1
        like_me.save()
        return True


class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return f"<character object: {self.first_name} ({self.id})>"

class Wish(models.Model):
    wish = models.CharField(max_length = 255)
    granted = models.BooleanField(default = False)
    granted_date = models.DateField(null=True, blank=True)
    desc = models.TextField()
    created_by = models.ForeignKey(User, related_name = 'my_wishes')
    liked_by = models.ManyToManyField(User, related_name = 'liked')
    likes = models.IntegerField(default = 0)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    objects = WishManager()

    def __repr__(self):
        return f"<character object: {self.wish} ({self.id})>"
