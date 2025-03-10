from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Documento

@csrf_exempt
def registrar_apertura(request, documento_id):
    documento = Documento.objects.get(id=documento_id)
    documento.fue_abierto = True
    documento.save()
    
    # Devuelve una imagen de 1x1 píxel transparente
    imagen_transparente = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3B'
    return HttpResponse(imagen_transparente, content_type='image/gif')
