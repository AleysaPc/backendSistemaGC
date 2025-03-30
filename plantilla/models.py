from django.db import models
from correspondencia.models import TipoDocumento

# Create your models here.
class Plantilla(models.Model):
    id_plantilla = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    contenido = models.TextField()

    def __str__(self):
        return f"{self.nombre} - {self.tipo_documento.nombre}"