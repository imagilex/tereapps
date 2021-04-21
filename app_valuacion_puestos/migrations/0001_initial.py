# Generated by Django 3.0.7 on 2021-04-08 00:26

import app_valuacion_puestos.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor', models.CharField(max_length=200, unique=True)),
                ('posicion', models.PositiveSmallIntegerField(default=app_valuacion_puestos.models.get_next_posicion_factor)),
                ('ponderacion_nivel_1', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Ponderación nivel I')),
            ],
            options={
                'ordering': ['posicion', 'factor'],
            },
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel_multiplicador', models.PositiveSmallIntegerField(default=1)),
                ('nivel', models.CharField(max_length=200)),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niveles', to='app_valuacion_puestos.Factor')),
            ],
            options={
                'ordering': ['nivel_multiplicador'],
            },
        ),
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puesto', models.CharField(max_length=200, unique=True)),
                ('posicion', models.PositiveSmallIntegerField(default=app_valuacion_puestos.models.get_next_posicion_puesto)),
                ('estatus', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['posicion', 'puesto'],
            },
        ),
        migrations.CreateModel(
            name='Ponderacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puestos_ponderacion', to='app_valuacion_puestos.Nivel')),
                ('puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niveles_ponderacion', to='app_valuacion_puestos.Puesto')),
            ],
        ),
        migrations.AddField(
            model_name='nivel',
            name='puestos',
            field=models.ManyToManyField(through='app_valuacion_puestos.Ponderacion', to='app_valuacion_puestos.Puesto'),
        ),
        migrations.AlterUniqueTogether(
            name='nivel',
            unique_together={('factor', 'nivel')},
        ),
    ]