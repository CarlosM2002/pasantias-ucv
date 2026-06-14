from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirmar contraseña', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'role', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'password', 'first_name', 'gender', 'role', 'last_name', 'is_active',
            'is_staff'
        )

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    def role_display(self, obj):
        role = getattr(obj, 'role', None)
        if role == 'employee':
            return 'Pasante'
        if role == 'admin':
            return 'Administrador'
        if role == 'employer':
            tipo = getattr(obj, 'tipo_empresa', None)
            if tipo == 'dependencia':
                return 'Dependencia'
            return 'Empresa'
        return role

    role_display.short_description = 'Rol'

    list_display = ('email', 'first_name', 'last_name', 'gender', 'role_display', 'is_staff')
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'gender', 'role', )}),
        ('Permisos', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'first_name', 'last_name', 'gender', 'role', 'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)