from datetime import timedelta, datetime
from .models import WorkHour, TimeTrack
import string
import random
import base64
from config import settings
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime


def calculate_work_hours(queryset: TimeTrack):
    initial_time = datetime(year=2000, month=1, day=1, tzinfo=queryset[0].checkout_time.tzinfo)
    # initial_time = initial_time.replace(tzinfo=queryset[0].checkout_time.tzinfo)
    enters = []
    exits = []
    for checkout in queryset:
        if checkout.checkout_type == 'E':
            enters.append(checkout)
        else:
            exits.append(checkout)
    enters.sort(key=lambda x: x.checkout_time)
    exits.sort(key=lambda x: x.checkout_time)

    total_work_hours = 0
    for i, checkout in enumerate(enters):
        delta_time = exits[i].checkout_time - enters[i].checkout_time
        total_work_hours += delta_time.total_seconds()
        # WorkHour.objects.create(
        #     employee_id=checkout.employee_id,
        #     day=checkout.date,
        #     workhour=total_work_hours / 3600  
        # )
    return total_work_hours


def generate_random_string(length: int) -> str:
    return "".join(random.choice(string.ascii_letters) for i in range(length))


def encrypt_string(_string: str, BLOCK_SIZE: int = 32) -> str:
    key = settings.SECRET_KEY[:16]
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    return base64.b64encode(
        cipher.encrypt(pad(_string.encode("utf-8"), BLOCK_SIZE))
    ).decode("utf-8")


def decrypt_string(_string: str, BLOCK_SIZE: int = 32) -> str:
    key = settings.SECRET_KEY[:16]
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    return unpad(cipher.decrypt(base64.b64decode(_string)), BLOCK_SIZE).decode("utf-8")


def datetime_to_string(_datetime: datetime) -> str:
    return datetime.strftime(_datetime, "%Y-%m-%d %H:%M:%S")


def string_to_datetime(_datetime: datetime) -> datetime:
    return datetime.strptime(_datetime, "%Y-%m-%d %H:%M:%S")
