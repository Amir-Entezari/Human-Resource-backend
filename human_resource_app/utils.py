from datetime import timedelta,datetime
from .models import WorkHour,TimeTrack

def calculate_work_hours(queryset:TimeTrack):
    initial_time = datetime(year=2000,month=1,day=1,tzinfo=queryset[0].checkout_time.tzinfo)
    # initial_time = initial_time.replace(tzinfo=queryset[0].checkout_time.tzinfo)
    enters = []
    exits = []
    for checkout in queryset: 
        if checkout.checkout_type == 'E':
            enters.append(checkout)
        else:
            exits.append(checkout)
    enters.sort(key=lambda x:x.checkout_time)
    exits.sort(key=lambda x:x.checkout_time)

    total_work_hours = 0
    for i,checkout in enumerate(enters):
        delta_time = exits[i].checkout_time - enters[i].checkout_time 
        total_work_hours += delta_time.total_seconds()
        # WorkHour.objects.create(
        #     employee_id=checkout.employee_id,
        #     day=checkout.date,
        #     workhour=total_work_hours / 3600  
        # )
    return total_work_hours