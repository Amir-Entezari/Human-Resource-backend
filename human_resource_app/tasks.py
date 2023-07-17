from celery import shared_task
from datetime import datetime
from .models import TimeTrack,WorkHour,Employee
from django.db.models import F
# @shared_task
def update_workhour_table():
    timetrack = TimeTrack.objects.filter(checkout_time__date=datetime.today().date()).order_by("checkout_time")
    timetrack_len = len(timetrack)
    for i,checkout in enumerate(timetrack):
        if checkout.checkout_type == 'E':
            for j in range(i,timetrack_len):
                if timetrack[j].checkout_type == 'Q' and checkout.employee == timetrack[j].employee:
                    delta_time = (timetrack[j].checkout_time - checkout.checkout_time).total_seconds() / 3600
                    employee_work_hour=WorkHour.objects.filter(employee_id=checkout.employee,date=checkout.checkout_time.date()).last()
                    if employee_work_hour:
                        employee_work_hour.hours_worked += delta_time
                        employee_work_hour.save()
                    else:
                        WorkHour.objects.create(employee=checkout.employee,date=checkout.checkout_time,hours_worked=delta_time)

