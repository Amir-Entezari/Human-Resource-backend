from ninja import ModelSchema
from .models import TimeTrack,Employee
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