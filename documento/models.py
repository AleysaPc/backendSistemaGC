from django.db import models
from correspondencia.models import Correspondencia
import os

def ruta_archivo(instance, filename):
    if instance.tipo == 'enviado':
        return os.path.join('documentos','enviados', filename)
    elif instance.tipo == 'recibido':
        return os.path.join('documentos','recibido', filename)

# Create your models here.
class Documento(models.Model):
    TIPO_CHOICES = [('enviado', 'Enviado'),
                    ('recibido', 'Recibido'),]
    
    archivo = models.FileField(upload_to='ruta_archivo')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    nombre_archivo = models.CharField(max_length=255, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    tamano_archivo = models.IntegerField()
    contenido_extraido = models.TextField(null=True, blank=True)
    #fue_abierto = models.BooleanField(default=False)  # Campo para rastrear aperturas
    

    def __str__(self):
        return self.nombre_archivo
class ContenidoDocumento(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    fecha_procesamiento = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)