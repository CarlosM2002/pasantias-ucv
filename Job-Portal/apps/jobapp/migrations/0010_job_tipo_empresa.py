from django.db import migrations, models


def populate_tipo_empresa(apps, schema_editor):
    Job = apps.get_model('jobapp', 'Job')
    for job in Job.objects.select_related('user').all():
        if job.user and hasattr(job.user, 'tipo_empresa'):
            job.tipo_empresa = job.user.tipo_empresa
            job.save(update_fields=['tipo_empresa'])


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0009_salary_boolean_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='tipo_empresa',
            field=models.CharField(choices=[('dependencia', 'Dependencia'), ('empresa_externa', 'Empresa Externa')], max_length=20, null=True, blank=True),
        ),
        migrations.RunPython(populate_tipo_empresa, reverse_code=migrations.RunPython.noop),
    ]
