from django import forms
from account.constants import TIPO_EMPRESA
from account.models import User, EmployeeProfile, EmployerProfile

class EmployeeProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ingrese su nombre'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ingrese su apellido'})
        
    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender"]

class EmployerProfileEditForm(forms.ModelForm):
    tipo_empresa = forms.ChoiceField(
        required=False,
        label='Tipo de empresa',
        choices=TIPO_EMPRESA,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super(EmployerProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombre de la empresa'
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ingrese el nombre de la empresa'})
        if self.instance and getattr(self.instance, 'tipo_empresa', None):
            self.fields['tipo_empresa'].initial = self.instance.tipo_empresa

    class Meta:
        model = User
        fields = ["first_name", "tipo_empresa"]

class EmployeeProfileForm(forms.ModelForm):
    cedula = forms.CharField(required=False, label='Cédula', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 01234567'}))

    class Meta:
        model = EmployeeProfile
        fields = ["cedula", "resume", "bio", "skills"]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }

class EmployerProfileForm(forms.ModelForm):
    location = forms.CharField(
        required=False,
        label='Ubicación',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la ubicación de la empresa'})
    )
    company_website = forms.URLField(
        required=False,
        label='Sitio web de la empresa',
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el sitio web de la empresa'})
    )
    company_logo = forms.ImageField(
        required=False,
        label='Logo de la empresa',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    description = forms.CharField(
        required=False,
        label='Descripción de la empresa',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cuéntanos sobre tu empresa...'})
    )
    
    class Meta:
        model = EmployerProfile
        fields = ["company_website", "company_logo", "description"]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about your company...'}),
        }

