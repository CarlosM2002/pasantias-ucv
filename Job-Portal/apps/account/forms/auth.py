from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from account.models import User, EmployeeProfile
from account.constants import TIPO_EMPRESA
from django.core.validators import RegexValidator


class EmployeeRegistrationForm(UserCreationForm):
    cedula = forms.CharField(
        required=True,
        label='Cédula',
        max_length=8,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 01234567'}),
        validators=[RegexValidator(r'^\d{8}$', 'La cédula debe tener 8 dígitos')]
    )

    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "Nombre :"
        self.fields['last_name'].label = "Apellido :"
        self.fields['password1'].label = "Contraseña :"
        self.fields['password2'].label = "Confirmar Contraseña :"
        self.fields['email'].label = "Correo Electrónico :"
        self.fields['gender'].label = "Género :"

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ingrese su nombre'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ingrese su apellido'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Ingrese su correo electrónico'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Ingrese su contraseña'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirme su contraseña'})
        self.fields['cedula'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'gender']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employee"
        if commit:
            user.save()
            profile, _ = EmployeeProfile.objects.get_or_create(user=user)
            ced = self.cleaned_data.get('cedula')
            if ced:
                profile.cedula = ced
                profile.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        # Run Django's password validators and translate 'too short' message
        try:
            if password1:
                validate_password(password1, user=None)
        except DjangoValidationError as e:
            messages = []
            for err in e.error_list:
                code = getattr(err, 'code', '')
                msg = str(err)
                if code == 'password_too_short' or 'too short' in msg.lower():
                    messages.append('La contraseña es demasiado corta. Debe contener al menos 8 caracteres.')
                else:
                    messages.append(msg)
            raise forms.ValidationError(messages)
        return password2


class EmployerRegistrationForm(UserCreationForm):
    tipo_empresa = forms.ChoiceField(
        choices=TIPO_EMPRESA,
        label="Tipo de Empresa",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['tipo_empresa'].required = True
        self.fields['first_name'].label = "Nombre de la Empresa"
        self.fields['last_name'].label = "Dirección de la Empresa"
        self.fields['email'].label = "Correo Electrónico"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ingrese el nombre de la empresa', 'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ingrese la dirección de la empresa', 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Ingrese el correo electrónico', 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Ingrese la contraseña', 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirme la contraseña', 'class': 'form-control'})
        self.fields['tipo_empresa'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'tipo_empresa']

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        try:
            if password1:
                validate_password(password1, user=None)
        except DjangoValidationError as e:
            messages = []
            for err in e.error_list:
                code = getattr(err, 'code', '')
                msg = str(err)
                if code == 'password_too_short' or 'too short' in msg.lower():
                    messages.append('La contraseña es demasiado corta. Debe contener al menos 8 caracteres.')
                else:
                    messages.append(msg)
            raise forms.ValidationError(messages)
        return password2


class UserLoginForm(forms.Form):
    
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'})
    )
    
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(UserLoginForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super(UserLoginForm, self).clean(*args, **kwargs)
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("El usuario no existe.")

            if not user.check_password(password):
                raise forms.ValidationError("La contraseña no coincide.")

            if not user.is_active:
                raise forms.ValidationError("El usuario no está activo.")

            self.user = user

        return cleaned_data

    def get_user(self):
        return self.user

