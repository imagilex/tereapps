# Generated by Django 3.0.7 on 2021-03-25 00:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.CharField(max_length=300)),
                ('url', models.URLField(max_length=500)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mis_favoritos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['usuario', 'etiqueta', 'url'],
                'permissions': [('view_mine_fav', 'Ver Mis Favoritos'), ('add_mine_fav', 'Agregar Mis Favoritos'), ('change_mine_fav', 'Actualizar Mis Favoritos'), ('delete_mine_fav', 'Eliminar Mis Favoritos')],
                'unique_together': {('usuario', 'url')},
            },
        ),
    ]
