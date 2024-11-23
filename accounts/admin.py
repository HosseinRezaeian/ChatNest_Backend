from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OtpList

admin.site.register(OtpList)


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'last_name', 'first_name', 'is_staff', 'is_active', 'is_superuser', 'phone_number')
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'last_name', 'first_name', 'is_staff', 'is_active', 'is_superuser', 'phone_number')
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
