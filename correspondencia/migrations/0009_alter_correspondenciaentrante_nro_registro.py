# Generated by Django 5.1.5 on 2025-02-24 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correspondencia', '0008_alter_correspondenciaentrante_nro_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correspondenciaentrante',
            name='nro_registro',
            field=models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True),
        ),
    ]
