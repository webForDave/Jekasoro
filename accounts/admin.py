
# core Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# accounts app 
from .forms import RegistrationForm, CustomUserChange
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = CustomUserChange
    list_display = ['email', 'username', 'date_joined']
    ordering = ['-date_joined']
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2')
        }),
    )
    fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('profile_picture', 'username', 'bio')
        }),
        ('Permissions', {
            'fields': ('groups', 'is_superuser', 'is_active', 'user_permissions')
        }),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)