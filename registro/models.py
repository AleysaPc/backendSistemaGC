from django.db import models


# Create your models here.
class Directorio(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    correo = models.EmailField()

    def __str__(self):
        return self.correo

class DatosRemitente(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class RegistroRecibido(models.Model):
    idrecibido = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True) 
    #Datos del Remitente
    remitente = models.ForeignKey(DatosRemitente, on_delete=models.CASCADE)
    #Datos del Documento
    referencia = models.CharField(max_length=100)
    fojas = models.IntegerField()
    adjunto = models.FileField(upload_to='adjunto/')
    detalle = models.TextField()
    entregado = models.BooleanField(default=False)
    destinatario = models.EmailField()

    def __str__(self):
        return  "Reg-00"+str(self.idrecibido) + ' - ' + (self.referencia) + ' - ' + (self.remitente.nombre) + ' - ' + (self.remitente.institucion) 
