from django.db import models
from usuarios.models import CustomUser

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
    estadoEntrega = models.BooleanField(default=False)
    destinatarios = models.ManyToManyField(CustomUser)
    estadoLectura = models.BooleanField(default=False)  # Si ha sido leído o no
    tipoDocumento = models.CharField(max_length=50, choices=[('Informe', 'Informe'), ('Contrato', 'Contrato'), ('Memorándum', 'Memorándum')])  # Añadir tipo de documento como opciones
    prioridad = models.CharField(max_length=10, choices=[('Alta', 'Alta'), ('Normal', 'Normal'), ('Baja', 'Baja')], default='Normal')  # Prioridad del documento
    comentarios = models.TextField(blank=True, null=True)  # Comentarios internos opcionales
    fechaLimite = models.DateField(null=True, blank=True)  # Fecha límite opcional


    def __str__(self):
        return  "Reg-00"+str(self.idrecibido) + ' - ' + (self.referencia) + ' - ' + (self.remitente.nombre) + ' - ' + (self.remitente.institucion) 
