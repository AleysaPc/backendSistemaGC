# Generated by Django 5.1.5 on 2025-02-22 02:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tipo', models.CharField(max_length=20)),
                ('descripcion', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Correspondencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrante', 'Entrante'), ('saliente', 'Saliente')], max_length=20)),
                ('cite', models.CharField(blank=True, max_length=50, null=True)),
                ('nro_registro', models.CharField(blank=True, max_length=50, null=True)),
                ('referencia', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('paginas', models.IntegerField()),
                ('adjunto', models.TextField()),
                ('prioridad', models.CharField(choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')], max_length=20)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_recepcion', models.DateTimeField(blank=True, null=True)),
                ('fecha_limite_respuesta', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(max_length=50)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cliente.cliente')),
                ('personal_destinatario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.personal')),
                ('tipo_documento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='correspondencia.tipodocumento')),
            ],
        ),
        migrations.CreateModel(
            name='FlujoAprobacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_revision', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(max_length=50)),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('correspondencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flujos_aprobacion', to='correspondencia.correspondencia')),
                ('revisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.personal')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.TextField()),
                ('fecha_notificacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(max_length=50)),
                ('personal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones', to='usuarios.personal')),
            ],
        ),
    ]
