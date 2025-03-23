from documento.models import Documento, ContenidoDocumento
from rest_framework import serializers

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'

class ContenidoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoDocumento
        fields = '__all__'