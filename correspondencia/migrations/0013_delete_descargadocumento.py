# Generated by Django 5.1.5 on 2025-03-21 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correspondencia', '0012_remove_correspondenciasaliente_ultimo_cite'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DescargaDocumento',
        ),
    ]
