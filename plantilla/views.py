from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Plantilla
from .serializers import PlantillaSerializer

# Create your views here.
class PlantillaView(viewsets.ModelViewSet):
    queryset = Plantilla.objects.all()
    serializer_class = PlantillaSerializer
    #permission_classes = [permissions.IsAuthenticated] para que solo los usuarios autenticados puedan acceder a las vistas