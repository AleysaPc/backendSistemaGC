# Generated by Django 5.1.5 on 2025-03-09 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correspondencia', '0010_alter_correspondenciaentrante_nro_registro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correspondencia',
            name='tipo_documento',
        ),
    ]
