from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login
from ninja import Router
from ninja.errors import HttpError
from ninja.security import django_auth
from .models import TimeTrack, Employee, CustomUser
from .schemas import TimeTrackIn,TimeTrackOut,EmployeeCreateInOut,EmployeeRetrieve,UserRetrieve
from .utils import calculate_work_hours
from datetime import date
router = Router()

@router.post("/employees/TimeTrack/checkout",response=TimeTrackOut)
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

@router.post("/employees/create",response=EmployeeCreateInOut,auth=django_auth)
def create_employee(request:HttpRequest,payload:EmployeeCreateInOut):
    new_employee = Employee.objects.filter(personal_id=payload.personal_id)
    if not new_employee:
        new_employee = Employee(user_id=payload.user,personal_id=payload.personal_id,position=payload.position,joined_at=payload.joined_at,department_id=payload.department)
        new_employee.save()
        return new_employee
    else:
        return HttpResponse("Employee exists")

@router.get("/employees",response=list[EmployeeRetrieve])
def get_all_employees(request:HttpRequest):
    employees = Employee.objects.all()
    return employees

@router.get("/employees/{personal_id}",response=EmployeeRetrieve,auth=django_auth)
def get_employee(request:HttpRequest,personal_id):
    try:
        employee = Employee.objects.get(personal_id=personal_id)
        if not request.user.is_superuser : 
            if employee.personal_id != personal_id:
                return HttpResponse("you don't have access to this user information")
        return employee 
    except Employee.DoesNotExist:
        return HttpResponse("Employee does not exist with this personal id")
    

@router.get("/employees/{personal_id}/workhour")
def get_employee_workhour(request:HttpRequest,personal_id,start_date:date,end_date:date):
    employee_time_track = TimeTrack.objects.filter(employee__personal_id=personal_id,checkout_time__range=[start_date, end_date])
    total_hour = round(calculate_work_hours(employee_time_track) / 3600,ndigits=2)
    return {"total_hour":total_hour}