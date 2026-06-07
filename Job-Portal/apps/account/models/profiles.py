from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator

class EmployeeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    cedula = models.CharField(max_length=8, blank=True, null=True, validators=[RegexValidator(r'^\d{8}$', 'La cédula debe tener 8 dígitos')])
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    bio = models.TextField(blank=True)
    skills = TaggableManager(blank=True)

    def __str__(self):
        return f"Profile for {self.user.email}"

class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_profile')
    company_website = models.URLField(blank=True)
    company_logo = models.ImageField(upload_to='logos/', blank=True)
    description = models.TextField(blank=True)
    privilegios = models.BooleanField(default=False)

    def __str__(self):
        return f"Employer Profile for {self.user.email}"
