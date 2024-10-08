from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.db import models

# Create your models here


class Department(models.Model):
    department_name = models.CharField(max_length=255)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    def __str__(self):
        return self.department_name

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
    hour_wage = models.FloatField()
    def __str__(self):
        return self.user.username
class TimeTrack(models.Model):
    CHECKOUT_ENTER = 'E'
    CHECKOUT_QUIT = 'Q'
    CHECKOUT_CHOICES = [
        (CHECKOUT_ENTER, 'Enter'),
        (CHECKOUT_QUIT, 'Quit')
    ]
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    checkout_time = models.DateTimeField(auto_now_add=True)
    checkout_type = models.CharField(max_length=1, choices=CHECKOUT_CHOICES, default=CHECKOUT_ENTER)

class WorkHour(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    hours_worked = models.FloatField()
    def __str__(self):
        return self.date

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
    from_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='from_user'  # Add a related_name for the reverse accessor of from_user
    )
    to_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='to_user'  # Add a related_name for the reverse accessor of to_user
    )
    message = models.TextField()

class Device(models.Model):
    device_name = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    def __str__(self):
        return self.device_name