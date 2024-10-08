from ninja import ModelSchema,Schema
from .models import TimeTrack,Employee, CustomUser,Feedback
class TimeTrackIn(Schema):
    personal_id : str
class TimeTrackOut(ModelSchema):
    class Config:
        model = TimeTrack
        model_fields = [ "employee", "checkout_time","checkout_type"]

class EmployeeCreateInOut(ModelSchema):
    class Config:
        model = Employee
        model_fields = ["user","personal_id","position","joined_at","department","hour_wage"]

class EmployeeRetrieve(ModelSchema):
    class Config:
        model = Employee
        model_fields = ["user","personal_id","position","joined_at","department"]

class EmployeeInfo(Schema):
    first_name: str
    last_name: str
    personal_id:str
    time_track:list[TimeTrackOut]
    work_hours:list[dict]
    total_hours_worked: int
    total_wage: float
    feedbacks: list[dict]
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

class FeedbackIn(ModelSchema):
    class Config:
        model = Feedback
        model_fields = ["to_user","message"]