from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CustomUser,
    Employee,
    Department,
    TimeTrack,
    Feedback,
    Device,
    WorkHour,
)


# Register your models here.
@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )
    list_display = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_superuser",
    ]


@admin.register(Employee)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "user_id",
        "personal_id",
        "phone",
        "gender",
        "department",
        "joined_at",
        "hour_wage",
    ]
    list_select_related = ["user"]


@admin.register(Department)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "department_name"]


@admin.register(TimeTrack)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "employee", "checkout_time", "checkout_type"]


@admin.register(Feedback)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "from_user", "to_user", "message"]


@admin.register(Device)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "device_name", "ip_address", "department"]


@admin.register(WorkHour)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "employee", "hours_worked"]
