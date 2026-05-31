from django import forms

from jobapp.models import Job


class JobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Título :"
        self.fields['location'].label = "Ubicación :"
        self.fields['salary'].label = "Remuneración :"
        self.fields['work_mode'].label = "Modalidad :"
        self.fields['experience_level'].label = "Nivel de Experiencia :"
        self.fields['description'].label = "Descripción de la Oferta :"
        self.fields['tags'].label = "Etiquetas :"
        self.fields['last_date'].label = "Fecha Límite de Envío :"
        self.fields['company_name'].label = "Nombre de la Empresa :"
        self.fields['url'].label = "Página web :"

        self.fields['title'].widget.attrs.update({'placeholder': 'Por ejemplo: Desarrollador de Software'})
        self.fields['location'].widget.attrs.update({'placeholder': 'Por ejemplo: Chacao'})
        self.fields['salary'].widget.attrs.update({'placeholder': '$800 - $1200'})
        self.fields['tags'].widget.attrs.update(
            {'placeholder': 'Use comma separated. eg: Python, JavaScript '}
        )
        self.fields['last_date'].widget.attrs.update({'placeholder': 'YYYY-MM-DD '})
        self.fields['company_name'].widget.attrs.update({'placeholder': 'Nombre de la empresa'})
        self.fields['url'].widget.attrs.update({'placeholder': 'https://ejemplo.com'})

    class Meta:
        model = Job
        fields = [
            "title",
            "location",
            "job_type",
            "work_mode",
            "experience_level",
            "category",
            "salary",
            "description",
            "tags",
            "last_date",
            "company_name",
            "company_description",
            "url",
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')
        if not job_type:
            raise forms.ValidationError("Service is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("category is required")
        return category

    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:
            job.save()
        return job


class JobEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Título :"
        self.fields['location'].label = "Ubicación :"
        self.fields['salary'].label = "Remuneración :"
        self.fields['work_mode'].label = "Modalidad :"
        self.fields['description'].label = "Descripción de la Oferta :"
        self.fields['last_date'].label = "Fecha Límite de solicitud :"
        self.fields['company_name'].label = "Nombre de la Empresa :"
        self.fields['url'].label = "Página web :"

        self.fields['title'].widget.attrs.update({'placeholder': 'Por ejemplo: Desarrollador de Software'})
        self.fields['location'].widget.attrs.update({'placeholder': 'Por ejemplo: Chacao'})
        self.fields['salary'].widget.attrs.update({'placeholder': '$800 - $1200'})
        self.fields['last_date'].widget.attrs.update({'placeholder': 'YYYY-MM-DD '})
        self.fields['company_name'].widget.attrs.update({'placeholder': 'Nombre de la empresa'})
        self.fields['url'].widget.attrs.update({'placeholder': 'https://ejemplo.com'})

        self.fields['last_date'] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Service Name',
                    'class': 'datetimepicker1',
                }
            )
        )

    class Meta:
        model = Job
        fields = [
            "title",
            "location",
            "job_type",
            "work_mode",
            "salary",
            "description",
            "last_date",
            "company_name",
            "company_description",
            "url",
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')
        if not job_type:
            raise forms.ValidationError("Job Type is required")
        return job_type

    def save(self, commit=True):
        job = super(JobEditForm, self).save(commit=False)
        if commit:
            job.save()
        return job

