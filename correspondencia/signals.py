from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from .models import CorrespondenciaEntrante, CorrespondenciaSaliente
import os

@receiver(post_save, sender=CorrespondenciaEntrante)
def enviar_notificacion_correo(sender, instance, created, **kwargs):
    
    nro_registro = instance.nro_registro
    referencia = instance.referencia

    if created:  # Solo si se crea un nuevo documento
        print("Documento creado")

    if instance.fecha_respuesta is not None:
        fecha_respuesta_formateada = instance.fecha_respuesta.strftime('%d/%m/%Y %H:%M')
    else:
        fecha_respuesta_formateada = None  # O simplemente omite el formateo

    # Aquí puedes continuar con el envío de la notificación
    if fecha_respuesta_formateada:
        print(f"Notificación enviada. Fecha de respuesta: {fecha_respuesta_formateada}")
    else:
        print("Notificación enviada. Fecha de respuesta: No especificada")
        #Para adjuntar el documento
        documento = instance.documento.archivo.path if instance.documento else None

        remitente = instance.remitente
        if remitente:  # Verifica si remitente no es None
            nombre_remitente = f"{remitente.nombre} {remitente.apellido}"
            cargo_remitente = remitente.cargo
        
            if remitente.institucion:
                empresa_remitente = remitente.institucion.nombre_institucion
            else:
                empresa_remitente = 'No especificado'
        else:
            nombre_remitente = 'No especificado'
            cargo_remitente = 'No especificado'
            empresa_remitente = 'No especificado'


        # Construye el asunto y el mensaje del correo
        asunto = f'Nuevo documento registrado: {nro_registro}'
        mensaje = f'Se ha registrado un nuevo documento con los siguientes detalles:\n\n'
        mensaje += f'Número de registro: {nro_registro}\n'
        mensaje += f'Referencia: {referencia}\n'
        mensaje += f'Remitente: {nombre_remitente}\n'
        mensaje += f'Cargo: {cargo_remitente}\n'
        mensaje += f'Empresa: {empresa_remitente}\n'
        mensaje += f'Fecha límite de respuesta: {fecha_respuesta_formateada}\n'
        
        # Lista de destinatarios
        destinatarios = ['isabella172813@gmail.com']

        # Envía el correo electrónico
        email = EmailMessage (
            asunto,
            mensaje,
            'isatest172813@gmail.com',  # Remitente
            destinatarios,  # Lista de destinatarios
           
        )
        
         # Adjunta el documento al correo
        if instance.documento:  # Verifica si el documento existe
             archivo = instance.documento.archivo  # Accede al archivo relacionado
        if archivo:  # Verifica si el archivo está presente
            email.attach_file(archivo.path)  # Adjunta el archivo

        # Envía el correo electrónico
        try:
            email.send(fail_silently=True) 
        except Exception as e:
             print(f"Error al enviar el correo: {e}")
        

@receiver(post_save, sender=CorrespondenciaSaliente)
def enviar_notificacion_correo(sender, instance, created, **kwargs):
    # Solo proceder si el estado es 'en_revision'
    if instance.estado == "en_revision":  # Ahora sí envía la notificación en este estado
        cite = instance.cite
        referencia = instance.referencia
        remitente = instance.remitente
        estado = instance.estado

        if remitente:  # Verifica si remitente no es None
            nombre_remitente = f"{remitente.nombre} {remitente.apellido}"
            cargo_remitente = remitente.cargo
            empresa_remitente = remitente.institucion.nombre if remitente.institucion else 'No especificado'
        else:
            nombre_remitente = 'No especificado'
            cargo_remitente = 'No especificado'
            empresa_remitente = 'No especificado'

        # Construye el asunto y el mensaje del correo
        asunto = f'Nuevo documento elaborado: {cite}'
        mensaje = f'Se ha elaborado un nuevo documento con los siguientes detalles:\n\n'
        mensaje += f'Nro. CITE: {cite}\n'
        mensaje += f'Referencia: {referencia}\n'
        mensaje += f'Remitente: {nombre_remitente}\n'
        mensaje += f'Cargo: {cargo_remitente}\n'
        mensaje += f'Empresa: {empresa_remitente}\n'
        mensaje += f'Estado: {estado}\n'


        # Lista de destinatarios
        destinatarios = ['isabella172813@gmail.com']

        # Envía el correo electrónico
        email = EmailMessage(
            asunto,
            mensaje,
            'isatest172813@gmail.com',  # Remitente
            destinatarios,  # Lista de destinatarios
        )

        # Adjunta el documento al correo si existe
        if instance.archivo_word:  # Verifica si hay un archivo cargado
            ruta_documento = os.path.join(settings.MEDIA_ROOT, instance.archivo_word.name)  
            print(f"Intentando adjuntar archivo: {ruta_documento}")  # Para depuración
            
            if os.path.exists(ruta_documento):  # Verifica si la ruta es válida
                email.attach_file(ruta_documento)
                print("✅ Archivo adjuntado correctamente.")
            else:
                print("⚠ Archivo no encontrado. Verifica la ruta.")

        # Envía el correo electrónico
        try:
            email.send(fail_silently=True) 
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

        

    