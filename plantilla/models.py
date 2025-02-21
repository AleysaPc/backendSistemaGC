from django.db import models
from correspondencia.models import TipoDocumento

# Create your models here.
class Plantilla(models.Model):
    nombre_plantilla = models.CharField(max_length=100)
    contenido = models.TextField()
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, related_name='plantillas')