from correspondencia.models import Correspondencia, CorrespondenciaEntrante, CorrespondenciaSaliente
from rest_framework import serializers


class CorrespondenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correspondencia
        fields = '__all__'

class CorrespondenciaEntranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrespondenciaEntrante
        fields = '__all__'

class CorrespondenciaSalienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrespondenciaSaliente
        fields = '__all__'