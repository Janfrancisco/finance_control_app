from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "username", "full_name", "is_staff"]
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Informações Pessoais", {"fields": ("full_name", "avatar")}),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas Importantes", {"fields": ("date_joined",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "full_name", "avatar")}),
    )
    ordering = ["full_name"]

    readonly_fields = ("date_joined",)


admin.site.register(CustomUser, CustomUserAdmin)
