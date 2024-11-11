from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Definir los campos para el formulario de creación de usuarios
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name',),
        }),
    )

    # Definir los campos para el formulario de edición de usuarios
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture',)}),  # Agrega tu campo personalizado aquí
    )
