from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

class EmailAPIView(APIView):
    def post(self, request):
        try:
            to_email = "wil.fabri777@gmail.com"
            subject = "Correo de prueba"
            message = "Este es un correo de prueba desde DRF"
            send_mail(subject, message, None, [to_email])
            return Response({"message": "Email enviado"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error al enviar el correo"}, status=status.HTTP_400_BAD_REQUEST)

