from rest_framework import serializers
from .models import RegistroRecibido

class RegistroRecibidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroRecibido
        #fields = ['idrecibido', 'fecha', 'remitente', 'fojas', 'adjunto', 'detalle', 'entregado', 'destinatario']
        fields = '__all__' #todos los campos