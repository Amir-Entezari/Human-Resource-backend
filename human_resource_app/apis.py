from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login,logout
from ninja import Router
from ninja.errors import HttpError
from .models import TimeTrack, Employee, CustomUser, WorkHour
from .schemas import TimeTrackIn,TimeTrackOut,EmployeeCreateInOut,EmployeeRetrieve,UserOut,LoginIn
from .utils import calculate_work_hours
from .auth import user_auth,blacklist_token,generate_token
from datetime import date,datetime
router = Router()

@router.post("/employees/TimeTrack/checkout",response=TimeTrackOut)
def user_checkout(request: HttpRequest,payload:TimeTrackIn):
    checkout = TimeTrack.objects.filter(employee_id=payload.employee).order_by('checkout_time').last()
    new_checkout = None
    if checkout:
        if checkout.checkout_type == 'E':
            new_checkout = TimeTrack(employee_id= payload.employee, checkout_time=payload.checkout_time, checkout_type='Q')
            new_checkout.save()
            delta_time = (new_checkout.checkout_time - checkout.checkout_time).total_seconds() / 3600
            employee_work_hour=WorkHour.objects.filter(employee_id=payload.employee,date=payload.checkout_time.date()).last()
            if employee_work_hour:
                employee_work_hour.hours_worked += delta_time
                employee_work_hour.save()
            else:
                WorkHour.objects.create(employee_id=payload.employee,date=payload.checkout_time,hours_worked=delta_time)
        elif checkout.checkout_type == 'Q':
            new_checkout = TimeTrack(employee_id= payload.employee, checkout_time=payload.checkout_time, checkout_type='E')
            new_checkout.save()
    else:
        new_checkout = TimeTrack(employee_id= payload.employee, checkout_time=payload.checkout_time, checkout_type='E')
        new_checkout.save()

    return new_checkout

@router.post("/employees/create",response=EmployeeCreateInOut,auth=user_auth)
def create_employee(request:HttpRequest,payload:EmployeeCreateInOut):
    if request.user.is_staff:
        new_employee = Employee.objects.filter(personal_id=payload.personal_id)
        if not new_employee:
            new_employee = Employee(user_id=payload.user,
                                    personal_id=payload.personal_id,
                                    position=payload.position,
                                    joined_at=payload.joined_at,
                                    department_id=payload.department)
            new_employee.save()
            return new_employee
        else:
            return HttpError(409, f"Employee with the personal id of  already exist.")
    else:
        raise HttpError(403, "You can not create a employee. please login as admin.")

@router.get("/employees",response=list[EmployeeRetrieve])
def get_all_employees(request:HttpRequest):
    employees = Employee.objects.all()
    if not request.user.is_superuser : 
        raise HttpError(403,"You don't have access to this user information")
    return employees 

@router.get("/employees/{personal_id}",response=EmployeeRetrieve,auth=user_auth)
def get_employee(request:HttpRequest,personal_id):
    try:
        employee = Employee.objects.get(personal_id=personal_id)
        if not request.user.is_superuser : 
            if employee.personal_id != personal_id:
                raise HttpError(403,"You don't have access to this user information")
        return employee 
    except Employee.DoesNotExist:
        raise HttpError(404,"Employee does not exist with this personal id")
    

@router.get("/employees/{personal_id}/workhour")
def get_employee_workhour(request:HttpRequest,personal_id,start_date:date,end_date:date):
    employee_time_track = TimeTrack.objects.filter(employee__personal_id=personal_id,checkout_time__range=[start_date, end_date])
    if not employee_time_track:
        return {"Error": "No record was found in this date"}
    total_hour = round(calculate_work_hours(employee_time_track) / 3600,ndigits=2)
    return {"total_hour":total_hour}


@router.get("/user", response=UserOut, auth=user_auth)
def fetch_user(request: HttpRequest):
    if request.auth.is_authenticated:
        return request.auth
    else:
        raise HttpError(401, "User not authenticated")
    
@router.post("user/login")
def user_login(request: HttpRequest, payload:LoginIn) -> HttpResponse:
    try:
        user = CustomUser.objects.get(username=payload.username)
        if user.check_password(payload.password):
            login(request, user)
            return HttpResponse(generate_token(user), status=200) 
        else:
            return HttpResponse("Wrong username or password", status=401)
    except CustomUser.DoesNotExist:
        return HttpResponse("Wrong username or password", status=401)
    
@router.post("user/logout", auth=user_auth)
def user_logout(request):
    logout(request)
    blacklist_token(request.headers.get("Authorization"))