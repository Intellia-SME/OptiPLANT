from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SignupForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    add_fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
