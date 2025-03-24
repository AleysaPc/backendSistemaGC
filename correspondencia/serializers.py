from correspondencia.models import Correspondencia, CorrespondenciaEntrante, CorrespondenciaSaliente
from rest_framework import serializers


class CorrespondenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correspondencia
        fields = '__all__'

class CorrespondenciaEntranteSerializer(serializers.ModelSerializer):
    nombre_remitente = serializers.CharField(source='remitente.nombre', read_only=True)
    ruta = serializers.CharField(source='documento.archivo.url', read_only=True)

    class Meta:
        model = CorrespondenciaEntrante
        fields = [
            'id',
            'fecha_registro',
            'referencia',
            'descripcion',
            'paginas',
            'prioridad',
            'estado',
            'nro_registro',
            'fecha_recepcion',
            'fecha_respuesta',
            'remitente',
            'documento',
            'personal_destinatario',
            'nombre_remitente',
            'ruta'
        ]

class CorrespondenciaSalienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrespondenciaSaliente
        fields = '__all__'