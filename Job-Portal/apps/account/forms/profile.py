from django import forms
from account.models import User, EmployeeProfile, EmployerProfile

class EmployeeProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name'})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender"]

class EmployerProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployerProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombre de la empresa'
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ingrese el nombre de la empresa'})

    class Meta:
        model = User
        fields = ["first_name"]

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ["resume", "bio", "skills"]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }

class EmployerProfileForm(forms.ModelForm):
    COMPANY_TYPE_CHOICES = [
        ('externa', 'Externa'),
        ('dependencia', 'Dependencia'),
    ]

    location = forms.CharField(
        required=False,
        label='Ubicación',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la ubicación de la empresa'})
    )
    company_type = forms.ChoiceField(
        required=False,
        label='Tipo de empresa',
        choices=COMPANY_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
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

