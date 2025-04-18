from .models import Cliente,Institucion
from rest_framework import serializers

class ClienteSerializer(serializers.ModelSerializer):

    nombre_institucion = serializers.CharField(source='institucion.nombre_institucion', read_only=True)
    class Meta:
        model = Cliente
        fields = [
            "id",
            "nombre",
            "apellido",
            "cargo",
            "email",
            "nombre_institucion",
            "institucion",
        ]

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = '__all__'