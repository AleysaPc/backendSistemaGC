# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CorrespondenciaEntrante

@receiver(post_save, sender=CorrespondenciaEntrante)
def enviar_notificacion_correo(sender, instance, created, **kwargs):
    if created:  # Solo si se crea un nuevo documento
        # Verifica que los atributos existan antes de acceder a ellos
        nro_registro = getattr(instance, 'nro_registro', 'N/A')  # Usa 'N/A' si no existe
        referencia = getattr(instance, 'referencia', 'N/A')  # Usa 'N/A' si no existe
        

        # Construye el asunto y el mensaje del correo
        asunto = f'Nuevo documento registrado: {nro_registro}'
        mensaje = f'Se ha registrado un nuevo documento con los siguientes detalles:\n\n'
        mensaje += f'Número de registro: {nro_registro}\n'
        mensaje += f'Referencia: {referencia}\n'
        

        # Lista de destinatarios
        destinatarios = ['isabella172813@gmail.com']

        # Envía el correo electrónico
        send_mail(
            asunto,
            mensaje,
            'isatest172813@gmail.com',  # Remitente
            destinatarios,  # Lista de destinatarios
            fail_silently=False,
        )