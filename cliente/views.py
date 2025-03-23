from .models import Cliente, Institucion
from rest_framework import viewsets
from .serializers import ClienteSerializer, InstitucionSerializer

# Create your views here.
class ClienteView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class InstitucionView(viewsets.ModelViewSet):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
