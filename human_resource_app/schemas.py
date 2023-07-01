from ninja import ModelSchema
from .models import TimeTrack
class TimeTrackIn(ModelSchema):
    class Config:
        model = TimeTrack
        model_fields = [ "employee", "checkout_time"]
