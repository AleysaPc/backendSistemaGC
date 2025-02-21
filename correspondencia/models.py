from django.db import models

# Create your models here.
from django.db import models
from documento.models import Documento
from cliente.models import Cliente
from usuarios.models import Personal

class TipoDocumento(models.Model):
    nombre_tipo = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=255)

class Correspondencia(models.Model):
    TIPO_CHOICES = [('entrante', 'Entrante'), ('saliente', 'Saliente')]
    TIPO_CHOICES_PRIORIDAD = [('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cite = models.CharField(max_length=50, blank=True, null=True)
    nro_registro = models.CharField(max_length=50, blank=True, null=True)
    referencia = models.CharField(max_length=255)
    descripcion = models.TextField()
    paginas = models.IntegerField()
    adjunto = models.TextField()
    prioridad = models.CharField(max_length=20, choices=TIPO_CHOICES_PRIORIDAD)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_recepcion = models.DateTimeField(blank=True, null=True)
    fecha_limite_respuesta = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50)
    documento = models.ForeignKey(Documento, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    personal_destinatario = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True)

class FlujoAprobacion(models.Model):
    correspondencia = models.ForeignKey(Correspondencia, on_delete=models.CASCADE, related_name='flujos_aprobacion')
    revisor = models.ForeignKey(Personal, on_delete=models.CASCADE)
    fecha_revision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)
    comentarios = models.TextField(blank=True, null=True)

class Notificacion(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    fecha_notificacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)