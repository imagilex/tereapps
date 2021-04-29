# Generated by Django 3.0.7 on 2021-04-28 11:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_valuacion_puestos', '0008_puestoevaluacion_nombre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='puestoevaluacion',
            options={'ordering': ['puesto', '-updated']},
        ),
        migrations.RemoveField(
            model_name='puestoevaluacion',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='puestoevaluacion',
            name='created',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='puestoevaluacion',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]