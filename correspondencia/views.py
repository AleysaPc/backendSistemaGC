
from correspondencia.serializers import CorrespondenciaSerializer, CorrespondenciaEntranteSerializer,CorrespondenciaSalienteSerializer
from correspondencia.models import Correspondencia, CorrespondenciaEntrante, CorrespondenciaSaliente
from rest_framework import viewsets 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from plantilla.utils import generar_documento_word 

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

#Para generar el documento wordk
@csrf_exempt
def generar_documento(request, id):
    if request.method == "POST":
        try:
            correspondencia = Correspondencia.objects.get(id=id)
            response = generar_documento_word(correspondencia)  # Llamar a la función
            return response  # Esto debería devolver un archivo
        except Correspondencia.DoesNotExist:
            return JsonResponse({"error": "Correspondencia no encontrada"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)