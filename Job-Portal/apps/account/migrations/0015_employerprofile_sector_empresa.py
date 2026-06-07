from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_user_tipo_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerprofile',
            name='sector_empresa',
            field=models.CharField(blank=True, choices=[
                ('industria', 'Industria'),
                ('automotriz', 'Automotriz'),
                ('tecnologia', 'Tecnología'),
                ('salud', 'Salud'),
                ('finanzas', 'Finanzas'),
                ('comercio', 'Comercio'),
                ('energia', 'Energía'),
                ('telecomunicaciones', 'Telecomunicaciones'),
                ('construccion', 'Construcción'),
                ('logistica', 'Logística'),
            ], max_length=50, null=True),
        ),
    ]
