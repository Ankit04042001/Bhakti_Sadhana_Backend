from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone
from datetime import datetime

class User(AbstractUser):
    email = models.EmailField(max_length=50, blank=False, null=False, unique=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email



class Attendence(models.Model):
    attendence_status_choices = [
        ('P', 'Present'), 
        ('A', 'Absent'),
    ]
    date = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False)
    punch_in = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, editable=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, unique_for_date="date", default='')
    attendence_status = models.CharField(max_length=1, choices = attendence_status_choices, default = 'A')


    class Meta:
        unique_together = ['date', 'user']

    def __str__(self):
        return self.attendence_status

class Task(models.Model):
    task_heading = models.CharField(max_length = 100)
    task_description = models.TextField()

    def __str__(self):
        return self.task_heading


class Otp(models.Model):
    email = models.EmailField(editable=False, unique=True)
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    password = models.CharField(max_length=128, editable=False)
    count = models.SmallIntegerField(editable=False, default=0)
    otp = models.CharField(max_length=6, editable=False)
    in_time = models.TimeField(auto_now=False, auto_now_add=False, editable=False, default=datetime.now().strftime('%H:%M:%S'))


