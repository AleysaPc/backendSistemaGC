from rest_framework import serializers
from .models import Plantilla

class PlantillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantilla
        fields = '__all__'