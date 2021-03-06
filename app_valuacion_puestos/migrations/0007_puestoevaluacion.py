# Generated by Django 3.0.7 on 2021-04-28 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_valuacion_puestos', '0006_auto_20210427_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='PuestoEvaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('data', models.TextField()),
                ('puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='app_valuacion_puestos.Puesto')),
            ],
            options={
                'ordering': ['puesto', '-timestamp'],
            },
        ),
    ]
