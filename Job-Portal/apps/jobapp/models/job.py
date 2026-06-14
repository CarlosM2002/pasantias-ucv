from django.contrib.auth import get_user_model
from django.db import models
from django.core.cache import cache
from django.utils import timezone

from account.constants import TIPO_EMPRESA
from core.models import SoftDeleteModel, TimeStampedModel

from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

User = get_user_model()

JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)

WORK_MODE = (
    ('1', 'Remoto'),
    ('2', 'Hibrido'),
    ('3', 'Presencial'),
)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Job(TimeStampedModel, SoftDeleteModel):
    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
    title = models.CharField(max_length=300, db_index=True)
    description = CKEditor5Field(config_name='extends')
    tags = TaggableManager()
    location = models.CharField(max_length=300, db_index=True)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1, db_index=True)
    work_mode = models.CharField(choices=WORK_MODE, max_length=1, default='3')
    category = models.ForeignKey(Category, related_name='Category', on_delete=models.CASCADE)
    salary = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    company_name = models.CharField(max_length=300, db_index=True)
    tipo_empresa = models.CharField(choices=TIPO_EMPRESA, max_length=20, blank=True, null=True)
    priority = models.BooleanField(default=False)
    company_description = CKEditor5Field(config_name='extends', blank=True, null=True)
    url = models.URLField(max_length=200)
    last_date = models.DateField()
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.id:
            cache.delete(str(self.id))
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        now = timezone.now()
        self.applicant_set.filter(is_deleted=False).update(is_deleted=True, deleted_at=now)
        self.bookmarkjob_set.filter(is_deleted=False).update(is_deleted=True, deleted_at=now)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['title', 'location']),
            models.Index(fields=['is_published', 'is_closed']),
        ]

