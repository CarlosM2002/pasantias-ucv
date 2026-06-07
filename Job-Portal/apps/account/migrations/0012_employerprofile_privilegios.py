from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_employeeprofile_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerprofile',
            name='privilegios',
            field=models.BooleanField(default=False),
        ),
    ]
