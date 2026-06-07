from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0011_remove_experience_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='priority',
            field=models.BooleanField(default=False),
        ),
    ]
