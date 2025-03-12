from django.db import models

# Create your models here.
class Institucion (models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    email = models.EmailField()
    institucion = models.ForeignKey('cliente.Institucion', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo} - {self.institucion}"