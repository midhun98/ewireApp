from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users import models
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    filter_horizontal = ('groups', 'user_permissions')

    model = CustomUser
    list_display = ("username", "email", "is_staff", "is_active",)
    list_filter = ("is_staff", "is_active", "groups",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number", "profile_picture", "date")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone_number", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("username",)
    ordering = ("username",)


admin.site.register(models.CustomUser, CustomUserAdmin)