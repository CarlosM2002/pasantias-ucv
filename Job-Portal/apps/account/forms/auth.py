from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from account.models import User


class EmployeeRegistrationForm(UserCreationForm):
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
        return user


class EmployerRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "Nombre de la Empresa"
        self.fields['last_name'].label = "Dirección de la Empresa"
        self.fields['email'].label = "Correo Electrónico"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ingrese el nombre de la empresa'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ingrese la dirección de la empresa'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Ingrese el correo electrónico'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Ingrese la contraseña'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirme la contraseña'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


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
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("El usuario no existe.")

            if not user.check_password(password):
                raise forms.ValidationError("La contraseña no coincide.")

            if not user.is_active:
                raise forms.ValidationError("El usuario no está activo.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user

