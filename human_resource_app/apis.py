from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login
from ninja import Router
from ninja.errors import HttpError
from .models import TimeTrack, Employee
from .schemas import TimeTrackIn,TimeTrackOut,EmployeeCreateInOut
from ninja.security import django_auth

router = Router()

@router.post("/user/TimeTrack/checkout",response=TimeTrackOut)
def user_checkout(request: HttpRequest,payload:TimeTrackIn):
    checkout = TimeTrack.objects.all().order_by('checkout_time').last()
    new_checkout = None
    if checkout:
        if checkout.checkout_type == 'E':
            new_checkout = TimeTrack(employee_id= payload.employee, checkout_time=payload.checkout_time, checkout_type='Q')
            new_checkout.save()
        elif checkout.checkout_type == 'Q':
            new_checkout = TimeTrack(employee_id= payload.employee, checkout_time=payload.checkout_time, checkout_type='E')
            new_checkout.save()
    else:
        new_checkout = TimeTrack(employee_id= payload.employee, checkout_time=payload.checkout_time, checkout_type='E')
        new_checkout.save()

    return new_checkout

@router.post("/user/create",response=EmployeeCreateInOut,auth=django_auth)
def create_employee(request:HttpRequest,payload:EmployeeCreateInOut):
    new_employee = Employee.objects.filter(personal_id=payload.personal_id)
    if not new_employee:
        new_employee = Employee(user_id=payload.user,personal_id=payload.personal_id,position=payload.position,joined_at=payload.joined_at,department_id=payload.department)
        new_employee.save()
        return new_employee
    else:
        return HttpResponse("Employee exists")