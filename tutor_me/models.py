'''
REFERENCES

Title: GPT-3.5 Language Model
Author: OpenAI
Date: 2021-09
Code version: 3.5
URL: https://openai.com/
Software License: <OpenAI API Terms of Service>
Note: Used for the Django built in relationships
'''

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.contrib import admin


# Create your models here.
class Rate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)

# Some code from GPT-3.5 Language Model
class Course(models.Model):
    user = models.ManyToManyField(User)
    mnemonic = models.CharField(max_length=10, null=True)
    number = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=200, null=True)

# Some code from GPT-3.5 Language Model
class Appointment(models.Model):
     availability = models.ForeignKey(Availability, null=True, on_delete=models.CASCADE)
     course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
     student = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
     start = models.DateTimeField(default=timezone.now)
     end = models.DateTimeField(default=timezone.now)
     confirmed = models.BooleanField(default=False)
     note = models.CharField(max_length=200, null=True)


class RequestNotification(models.Model):
    student = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    notification = models.CharField(max_length=200, null=True)