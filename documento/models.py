from django.db import models

from correspondencia.models import Correspondencia


# Create your models here.
class Documento(models.Model):
    archivo = models.FileField(upload_to='documentos/')
    nombre_archivo = models.CharField(max_length=255, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    tamano_archivo = models.IntegerField()
    contenido_extraido = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return self.nombre_archivo
class ContenidoDocumento(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    fecha_procesamiento = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)