# Generated by Django 3.0.7 on 2021-04-28 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_valuacion_puestos', '0007_puestoevaluacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='puestoevaluacion',
            name='nombre',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]