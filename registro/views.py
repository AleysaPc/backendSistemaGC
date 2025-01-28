from rest_framework import viewsets
from registro.serializers import RegistroRecibidoSerializer
from .models import RegistroRecibido


# Create your views here.
class RegistroRecibidoView(viewsets.ModelViewSet):
    serializer_class = RegistroRecibidoSerializer
    queryset = RegistroRecibido.objects.all()
    
