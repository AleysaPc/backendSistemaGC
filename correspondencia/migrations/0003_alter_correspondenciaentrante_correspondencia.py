# Generated by Django 5.1.5 on 2025-02-24 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correspondencia', '0002_correspondencia_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correspondenciaentrante',
            name='correspondencia',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='BandejadeEntrada', to='correspondencia.correspondencia'),
        ),
    ]
