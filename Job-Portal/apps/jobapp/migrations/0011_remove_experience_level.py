from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0010_job_tipo_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='experience_level',
        ),
    ]
