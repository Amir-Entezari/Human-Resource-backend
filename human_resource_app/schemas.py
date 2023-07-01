from ninja import ModelSchema
from .models import TimeTrack
class TimeTrackEntry(ModelSchema):
    class Config:
        model = TimeTrack
        model_fields = [ "employee", "checkout_time","checkout_type"]
