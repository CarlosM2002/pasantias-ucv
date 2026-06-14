

import re
from django.db import migrations, models


def migrate_salary_to_boolean(apps, schema_editor):
    Job = apps.get_model('jobapp', 'Job')
    for job in Job.objects.all():
        raw_salary = getattr(job, 'salary', None)
        boolean_salary = False
        if raw_salary:
            salary_text = str(raw_salary).strip()
            if salary_text:
                found_numbers = re.findall(r'\d+', salary_text)
                for number in found_numbers:
                    try:
                        if int(number) > 0:
                            boolean_salary = True
                            break
                    except ValueError:
                        continue
        job.salary_bool = boolean_salary
        job.save(update_fields=['salary_bool'])


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0008_alter_job_tags_alter_job_work_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='salary_bool',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(migrate_salary_to_boolean, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='job',
            name='salary',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='salary_bool',
            new_name='salary',
        ),
    ]
