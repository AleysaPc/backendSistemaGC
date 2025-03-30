
from correspondencia.serializers import CorrespondenciaSerializer, CorrespondenciaEntranteSerializer,CorrespondenciaSalienteSerializer
from correspondencia.models import Correspondencia, CorrespondenciaEntrante, CorrespondenciaSaliente
from rest_framework import viewsets 
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from plantilla.utils import generar_documento_word
from rest_framework.pagination import PageNumberPagination

# Definir una clase de paginación personalizada si quieres ajustar el tamaño de la página y el comportamiento
class PaginacionPersonalizada(PageNumberPagination):
    page_size = 10  # Número predeterminado de elementos por página
    page_size_query_param = 'page_size'  # Permitir cambiar el tamaño de la página desde los parámetros de la consulta
    max_page_size = 100  # Tamaño máximo de página permitido

# Create your views here.
class CorrespondenciaView(viewsets.ModelViewSet):
    queryset = Correspondencia.objects.all()
    serializer_class = CorrespondenciaSerializer

class CorrespondenciaEntranteView(viewsets.ModelViewSet):
    serializer_class = CorrespondenciaEntranteSerializer
    queryset = CorrespondenciaEntrante.objects.all().order_by('id_correspondencia_entrante')

    pagination_class = PaginacionPersonalizada

    def list(self, request, *args, **kwargs):
        all_data = request.query_params.get('all_data', 'false').lower() == 'true'  # Convierte a booleano correctamente

        if all_data:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)  # Usa la paginación normal

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