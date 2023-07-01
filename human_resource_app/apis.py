from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login
from ninja import Router
from ninja.errors import HttpError
from .models import TimeTrack
from .schemas import TimeTrackEntry

router = Router()

@router.post("/user/TimeTrack/checkout")
def user_checkout(request: HttpRequest):
    pass
