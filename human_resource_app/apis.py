from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login
from ninja import Router
from ninja.errors import HttpError
from .models import TimeTrack
from .schemas import TimeTrackIn,TimeTrackOut

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
