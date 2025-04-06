from correspondencia.models import Correspondencia, CorrespondenciaEntrante, CorrespondenciaSaliente
from rest_framework import serializers


class CorrespondenciaSerializer(serializers.ModelSerializer):
    nombre_remitente = serializers.CharField(source='remitente.nombre', read_only=True)
    class Meta:
        model = Correspondencia
        fields = [
            "id_correspondencia",
             "fecha_registro",
             "referencia",
             "descripcion",
             "paginas",
             "prioridad",
             "estado",
             "remitente",
             "nombre_remitente",
             "documento",
             "personal_destinatario"
        ]

class CorrespondenciaEntranteSerializer(serializers.ModelSerializer):
    nombre_remitente = serializers.CharField(source='remitente.nombre', read_only=True)
    ruta = serializers.CharField(source='documento.archivo.url', read_only=True)

    nombre_institucion = serializers.CharField(source='remitente.institucion.nombre_institucion', read_only=True)

    class Meta:
        model = CorrespondenciaEntrante
        fields = [
            'id_correspondencia_entrante',
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
            'nombre_institucion',
            'ruta'
        ]

class CorrespondenciaSalienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrespondenciaSaliente
        fields = '__all__'