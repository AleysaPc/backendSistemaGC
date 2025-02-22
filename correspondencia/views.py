from django.shortcuts import render

from correspondencia.serializers import CorrespondenciaSerializer
from correspondencia.models import Correspondencia
from rest_framework import viewsets 

# Create your views here.
class CorrespondenciaViewSet(viewsets.ModelViewSet):
    queryset = Correspondencia.objects.all()
    serializer_class = CorrespondenciaSerializer
