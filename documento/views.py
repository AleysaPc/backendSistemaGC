from documento.models import Documento, ContenidoDocumento
from documento.serializers import DocumentoSerializer, ContenidoDocumentoSerializer
from rest_framework import viewsets


class DocumentoView(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

class ContenidoDocumentoView(viewsets.ModelViewSet):
    queryset = ContenidoDocumento.objects.all()
    serializer_class = ContenidoDocumentoSerializer