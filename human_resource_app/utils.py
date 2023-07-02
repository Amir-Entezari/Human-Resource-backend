from datetime import timedelta
from .models import WorkHour,TimeTrack

def calculate_work_hours(queryset:TimeTrack):
    for checkout in queryset:
        total_work_hours = 0  
        if checkout.checkout_type == 'E':
            total_work_hours -= checkout.checkout_time
        else:
            total_work_hours += checkout.checkout_time

        WorkHour.objects.create(
            employee_id=checkout.employee_id,
            day=checkout.date,
            workhour=total_work_hours / 3600  
        )
