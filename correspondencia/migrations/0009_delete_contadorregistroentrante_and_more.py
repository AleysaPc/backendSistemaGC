# Generated by Django 5.1.5 on 2025-03-21 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correspondencia', '0008_rename_codigo_correspondenciainterna_cite_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ContadorRegistroEntrante',
        ),
        migrations.AddField(
            model_name='correspondenciaentrante',
            name='ultimo_registro',
            field=models.IntegerField(default=0),
        ),
    ]
