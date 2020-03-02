from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import re

# email validation - standard email format
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# password validation - At least 8 char, have 1 number, 1 lowercase, 1 uppercase
pw_regex = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}')

class BasicManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData["fname"]) < 1 or len(postData["lname"]) < 1:
            errors["name"] = "Please enter your name"
        if not email_regex.match(postData["email"]):
            errors["email"] = "Invalid email address"
        if not pw_regex.match(postData["confirm_pw"]):
            errors["confirm_pw"] = "Passwords must have at least 8 characters, 1 number, 1 lowercase, and 1 uppercase"
        if postData["pw"] != postData["confirm_pw"]:
            errors["pw_match"] = "Passwords do not match"
        if User.objects.filter(email = postData['email']):
            errors["email"] = "Email is already registered"
        return errors
    
    def trip_validator(self, postData):
        errors = {}
        if len(postData["destination"]) < 2:
            errors["destination"] = "A destination must be have at least 3 characters"
        if len(postData["plan"]) <= 0:
            errors["plan"] = "You should create a plan"
        if len(postData["start_date"]) > 0 and datetime.strptime(postData["start_date"], '%Y-%m-%d') < datetime.today():
            errors["start_date"] = "Trip dates should be in the future"
        if postData["start_date"] == "":
            errors["start_date"] = "Your trip needs a start date"
        if len(postData["end_date"]) > 0 and datetime.strptime(postData["end_date"], '%Y-%m-%d') < datetime.today():
            errors["end_date"] = "Trip dates should be in the future"
        if postData["end_date"] == "":
            errors["end_date"] = "Your trip needs an end date"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if not user:
            errors['email'] = "Email has not been registered"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BasicManager()

class Trip(models.Model):
    user = models.ForeignKey(User, related_name="trips", on_delete = models.CASCADE)
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BasicManager()
