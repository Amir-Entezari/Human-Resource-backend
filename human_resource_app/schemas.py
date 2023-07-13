from ninja import ModelSchema,Schema
from .models import TimeTrack,Employee, CustomUser
class TimeTrackIn(ModelSchema):
    class Config:
        model = TimeTrack
        model_fields = [ "employee", "checkout_time"]
class TimeTrackOut(ModelSchema):
    class Config:
        model = TimeTrack
        model_fields = [ "employee", "checkout_time","checkout_type"]

class EmployeeCreateInOut(ModelSchema):
    class Config:
        model = Employee
        model_fields = ["user","personal_id","position","joined_at","department"]

class EmployeeRetrieve(ModelSchema):
    class Config:
        model = Employee
        model_fields = ["user","personal_id","position","joined_at","department"]



class LoginIn(ModelSchema):
    class Config:
        model = CustomUser
        model_fields = [ "username", "password"]

class LogoutOut(ModelSchema):
    class Config:
        model = CustomUser
        model_fields = ["username", "email", "first_name", "last_name"]

class UserOut(ModelSchema):
    class Config:
        model = CustomUser
        model_fields = ["username", "email", "first_name", "last_name"]
