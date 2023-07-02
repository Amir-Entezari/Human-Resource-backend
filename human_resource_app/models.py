from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models

# Create your models here


class Department(models.Model):
    department_name = models.CharField(max_length=255)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    personal_id = models.IntegerField(unique=True,                                  
                                        validators=[
                                            RegexValidator(
                                                regex='^[0-9]{8}$',
                                                message='Personal ID must be an 8-digit number.',
                                                code='invalid_personal_id'
                                            ),]
            )
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
    checkout_time = models.DateTimeField(auto_now_add=True)
    checkout_type = models.CharField(max_length=1, choices=CHECKOUT_CHOICES, default=CHECKOUT_ENTER)

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username