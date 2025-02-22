from correspondencia.models import Correspondencia
from rest_framework import serializers


class CorrespondenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correspondencia
        fields = '__all__'