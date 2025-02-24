from django.db import models
from cliente.models import Cliente
from usuarios.models import Personal


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Correspondencia(models.Model):

    TIPO_CHOICES_PRIORIDAD = [('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')]

    fecha_registro = models.DateTimeField(auto_now_add=True)
    remitente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=255)
    descripcion = models.TextField()
    paginas = models.IntegerField()
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True)
    #documento = models.ForeignKey('documento.Documento', on_delete=models.SET_NULL, null=True, related_name="correspondencias_relacionadas")
    prioridad = models.CharField(max_length=20, choices=TIPO_CHOICES_PRIORIDAD)
    estado = models.CharField(max_length=50)
    personal_destinatario = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.tipo_documento} - {self.referencia}"
class CorrespondenciaEntrante(models.Model):
    nro_registro = models.CharField(max_length=50, blank=True, null=True)
    fecha_recepcion = models.DateTimeField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    correspondencia = models.OneToOneField(Correspondencia, on_delete=models.CASCADE, related_name='entrantes')
class CorrespondenciaSaliente(models.Model):
    cite = models.CharField(max_length=50, blank=True, null=True)
    fecha_hora_envio = models.DateTimeField(blank=True, null=True)
    fecha_hora_confirmacion_recepcion = models.DateTimeField(blank=True, null=True)
    fecha_proximo_seguimiento = models.DateTimeField(blank=True, null=True)
    correspondencia = models.OneToOneField(Correspondencia, on_delete=models.CASCADE, related_name='saliente')

class FlujoAprobacion(models.Model):

    ESTADO_CHOICES = [('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')]

    correspondencia = models.ForeignKey(Correspondencia, on_delete=models.CASCADE, related_name='flujos_aprobacion')
    revisor = models.ForeignKey(Personal, on_delete=models.CASCADE)
    fecha_revision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default="Pendiente")
    comentarios = models.TextField(blank=True, null=True)

class Notificacion(models.Model):

    ESTADO_NOTIFICACION_CHOICES = [('no_leido', 'No leido'), ('leido', 'Leido')]

    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    fecha_notificacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)