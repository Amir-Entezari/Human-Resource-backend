from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

# Create your models here


class Department(models.Model):
    department_name = models.CharField(max_length=255)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField( max_length=50)
    position = models.CharField(max_length=255)
    joined_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department)

class TimeTrack(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username