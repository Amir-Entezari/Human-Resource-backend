from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser,Employee,Department,TimeTrack
# Register your models here.
@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'first_name', 'last_name'),
            },
        ),
    )
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(TimeTrack)