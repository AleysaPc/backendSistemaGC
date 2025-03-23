
from correspondencia.serializers import CorrespondenciaSerializer, CorrespondenciaEntranteSerializer,CorrespondenciaSalienteSerializer
from correspondencia.models import Correspondencia, CorrespondenciaEntrante, CorrespondenciaSaliente
from rest_framework import viewsets 

# Create your views here.
class CorrespondenciaView(viewsets.ModelViewSet):
    queryset = Correspondencia.objects.all()
    serializer_class = CorrespondenciaSerializer

class CorrespondenciaEntranteView(viewsets.ModelViewSet):
    queryset = CorrespondenciaEntrante.objects.all()
    serializer_class = CorrespondenciaEntranteSerializer

class CorrespondenciaSalienteView(viewsets.ModelViewSet):
    queryset = CorrespondenciaSaliente.objects.all()
    serializer_class = CorrespondenciaSalienteSerializer

