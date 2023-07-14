from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login, logout
from ninja import Router
from ninja.errors import HttpError
from .models import TimeTrack, Employee, CustomUser, WorkHour, Feedback
from .schemas import (
    TimeTrackIn,
    TimeTrackOut,
    EmployeeCreateInOut,
    EmployeeRetrieve,
    UserOut,
    LoginIn,
    EmployeeInfo,
    FeedbackIn,
)
from .utils import calculate_work_hours
from .auth import user_auth, blacklist_token, generate_token
from datetime import date, datetime
import calendar

router = Router()


@router.get("/user", response=UserOut, auth=user_auth)
def fetch_user(request: HttpRequest):
    if request.auth.is_authenticated:
        return request.auth
    else:
        raise HttpError(401, "User not authenticated")


@router.post("user/login")
def user_login(request: HttpRequest, payload: LoginIn) -> HttpResponse:
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


@router.post("/employees/create", response=EmployeeCreateInOut, auth=user_auth)
def create_employee(request: HttpRequest, payload: EmployeeCreateInOut):
    if request.user.is_staff:
        new_employee = Employee.objects.filter(personal_id=payload.personal_id)
        if not new_employee:
            new_employee = Employee(
                user_id=payload.user,
                personal_id=payload.personal_id,
                position=payload.position,
                joined_at=payload.joined_at,
                department_id=payload.department,
                hour_wage=payload.hour_wage,
            )
            new_employee.save()
            return new_employee
        else:
            return HttpError(409, f"Employee with the personal id of  already exist.")
    else:
        raise HttpError(403, "You can not create a employee. please login as admin.")


@router.get("/employees")
def get_all_employees(request: HttpRequest):
    employees = Employee.objects.select_related("user").all()
    employees_list = []
    for employee in employees:
        current_date = datetime.now()
        start_date = current_date.replace(day=1)
        _, end_date = calendar.monthrange(current_date.year, current_date.month)
        end_date = current_date.replace(day=end_date)

        employee_time_track = TimeTrack.objects.filter(
            employee=employee,
            checkout_time__range=[start_date, end_date],
        )
        if not employee_time_track:
            continue
        total_hours_worked = round(
            calculate_work_hours(employee_time_track) / 3600, ndigits=2
        )
        employee_work_hour = WorkHour.objects.filter(employee=employee)
        employee_info = {
            "user_id": employee.user.id,
            "detail": {
                "username": employee.user.username,
                "email": employee.user.email,
                "first_name": employee.user.first_name,
                "last_name": employee.user.last_name,
                "personal_id": employee.personal_id,
                "phone": employee.phone,
                "gender": employee.gender,
                "position": employee.position,
                "joined_at": employee.joined_at,
                "department": employee.department.department_name,
                # "checkouts_list": list(employee_time_track),
                "work_hours": [
                    {"date": workhour.date, "hours_worked": workhour.hours_worked}
                    for workhour in employee_work_hour
                ],
                "total_hours_worked": total_hours_worked,
                "total_wage": total_hours_worked * employee.hour_wage,
            },
        }
        employees_list.append(employee_info)
    if not request.user.is_superuser:
        raise HttpError(403, "You don't have access to this user information")
    return employees_list


@router.get("/employees/{personal_id}", response=EmployeeInfo, auth=user_auth)
def get_employee(request: HttpRequest, personal_id):
    if (
        personal_id == "me"
        or Employee.objects.get(user_id=request.user.id).personal_id == personal_id
        or request.user.is_superuser
    ):
        try:
            employee = Employee.objects.get(user_id=request.user.id)
            current_date = datetime.now()
            start_date = current_date.replace(day=1)
            _, end_date = calendar.monthrange(current_date.year, current_date.month)
            end_date = current_date.replace(day=end_date)

            employee_time_track = TimeTrack.objects.filter(
                employee__personal_id=employee.personal_id,
                checkout_time__range=[start_date, end_date],
            )
            employee_work_hour = WorkHour.objects.filter(employee=employee)
            
            first_name = employee.user.first_name
            last_name = employee.user.first_name
            personal_id = employee.personal_id
            total_hours_worked = round(
                calculate_work_hours(employee_time_track) / 3600, ndigits=2
            )
            feedbacks = Feedback.objects.filter(to_user=employee.user)

            employee_info = {
                "first_name": first_name,
                "last_name": last_name,
                "personal_id": personal_id,
                "time_track": list(employee_time_track),
                "work_hours": [
                    {"date": workhour.date, "hours_worked": workhour.hours_worked}
                    for workhour in employee_work_hour
                ],
                "total_hours_worked": total_hours_worked,
                "total_wage": employee.hour_wage * total_hours_worked,
                "feedbacks": [
                    {"from": feedback.from_user.username, "message": feedback.message}
                    for feedback in feedbacks
                ],
            }

            return employee_info
        except Employee.DoesNotExist:
            raise HttpError(404, "Employee does not exist with this personal id")
    else:
        raise HttpError(403, "You don't have access to this user information")


@router.get("/employees/{personal_id}/workhour", auth=user_auth)
def get_employee_workhour(
    request: HttpRequest, personal_id, start_date: date, end_date: date
):
    if (
        personal_id == "me"
        or Employee.objects.get(user_id=request.user.id).personal_id == personal_id
        or request.user.is_superuser
    ):
        employee = Employee.objects.get(personal_id=personal_id)
        employee_time_track = TimeTrack.objects.filter(
            employee=employee,
            checkout_time__range=[start_date, end_date],
        )
        if not employee_time_track:
            return {"Error": "No record was found in this date"}
        total_hour = round(calculate_work_hours(employee_time_track) / 3600, ndigits=2)
        return {"total_hour": total_hour, "total_wage": total_hour * employee.hour_wage}
    else:
        raise HttpError(403, "You don't have access to this user information")


@router.post("/employees/TimeTrack/checkout", response=TimeTrackOut)
def user_checkout(request: HttpRequest, payload: TimeTrackIn):
    checkout = (
        TimeTrack.objects.filter(employee_id=payload.employee)
        .order_by("checkout_time")
        .last()
    )
    new_checkout = None
    if checkout:
        if checkout.checkout_type == "E":
            new_checkout = TimeTrack(
                employee_id=payload.employee,
                checkout_time=payload.checkout_time,
                checkout_type="Q",
            )
            new_checkout.save()
            delta_time = (
                new_checkout.checkout_time - checkout.checkout_time
            ).total_seconds() / 3600
            employee_work_hour = WorkHour.objects.filter(
                employee_id=payload.employee, date=payload.checkout_time.date()
            ).last()
            if employee_work_hour:
                employee_work_hour.hours_worked += delta_time
                employee_work_hour.save()
            else:
                WorkHour.objects.create(
                    employee_id=payload.employee,
                    date=payload.checkout_time,
                    hours_worked=delta_time,
                )
        elif checkout.checkout_type == "Q":
            new_checkout = TimeTrack(
                employee_id=payload.employee,
                checkout_time=payload.checkout_time,
                checkout_type="E",
            )
            new_checkout.save()
    else:
        new_checkout = TimeTrack(
            employee_id=payload.employee,
            checkout_time=payload.checkout_time,
            checkout_type="E",
        )
        new_checkout.save()

    return new_checkout


@router.post("feedback/send", auth=user_auth)
def send_feedback(request: HttpRequest, payload: FeedbackIn):
    try:
        to_user = CustomUser.objects.get(id=payload.to_user)
        new_feedback = Feedback.objects.create(
            from_user_id=request.user.id, to_user=to_user, message=payload.message
        )
        new_feedback.save()
        return HttpResponse("Feedback successfully sent", status=200)
    except CustomUser.DoesNotExist:
        raise HttpError(404, "User does not exist")
