from django.db import models
from django.apps import apps

# Create your models here.
class Documento(models.Model):
    correspondencia = models.ForeignKey('correspondencia.Correspondencia', on_delete=models.CASCADE, related_name="documentos")
    archivo = models.FileField(upload_to='documentos/')
    nombre_archivo = models.CharField(max_length=255)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    tipo_archivo = models.CharField(max_length=50)
    tamano_archivo = models.IntegerField()
    contenido_extraido = models.TextField(null=True, blank=True)

class ContenidoDocumento(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    fecha_procesamiento = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)