from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.db import models

# Create your models here


class Department(models.Model):
    department_name = models.CharField(max_length=255)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()

class Employee(models.Model):
    GENDER_MAKE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = [
        (GENDER_MAKE , 'M'),
        (GENDER_FEMALE , 'F')
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    personal_id = models.CharField(max_length=9,validators=[MinLengthValidator(9)])
    phone = models.CharField(max_length=11,validators=[MinLengthValidator(11)])
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    position = models.CharField(max_length=255)
    joined_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)

class TimeTrack(models.Model):
    CHECKOUT_ENTER = 'E'
    CHECKOUT_QUIT = 'Q'
    CHECKOUT_CHOICES = [
        (CHECKOUT_ENTER, 'Enter'),
        (CHECKOUT_QUIT, 'Quit')
    ]
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    checkout_time = models.DateTimeField()
    checkout_type = models.CharField(max_length=1, choices=CHECKOUT_CHOICES, default=CHECKOUT_ENTER)

class WorkHour(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    hours_worked = models.FloatField()

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username
    
class BlackToken(models.Model):
    token = models.CharField(
        verbose_name="Token to blacklist", max_length=60, null=False, blank=False
    )

class Feedback(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    text = models.TextField()