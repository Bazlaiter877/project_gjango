from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'phone_number', 'country', 'is_staff', 'is_active']
    ordering = ['email']
    search_fields = ['email', 'phone_number', 'country']
    list_filter = ['is_staff', 'is_active', 'country']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('phone_number', 'country', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'country', 'avatar', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
