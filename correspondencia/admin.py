from django.contrib import admin
from .models import Correspondencia, CorrespondenciaEntrante, CorrespondenciaSaliente, TipoDocumento
from django.core.mail import send_mail

# Configuración personalizada para CorrespondenciaEntrante
@admin.register(CorrespondenciaEntrante)
class CorrespondenciaEntranteAdmin(admin.ModelAdmin):
    # Excluye el campo nro_registro del formulario
    exclude = ('nro_registro',)

    # Si deseas mostrar el campo como de solo lectura, agrégalo a readonly_fields
    readonly_fields = ('nro_registro',)

    # Campos que se mostrarán en la lista de registros en el admin
    list_display = ('nro_registro', 'fecha_recepcion_formateada', 'fecha_respuesta_formateada', 'mostrar_referencia', 'mostrar_remitente')

    # Metodo para mostrar la referencia
    def mostrar_referencia(self, obj):
        # Acceder al campo 'referencia' del modelo relacionado 'Correspondencia'
        return obj.correspondencia.referencia
    mostrar_referencia.short_description = 'Referencia'

    #Metodo para mostrar remitente
    def mostrar_remitente(self, obj):
       remitente = obj.correspondencia.remitente
       institucion = remitente.institucion 
       return f"{remitente.nombre} - {institucion.nombre}"
    mostrar_remitente.short_description = 'Remitente'

    def fecha_recepcion_formateada(self, obj):
        if obj.fecha_recepcion:
            return obj.fecha_recepcion.strftime("%d-%m-%Y %H:%M")  # Formato: "01-03-2025 14:30"
        return ""
    fecha_recepcion_formateada.short_description = 'Fecha de Recepción'

    def fecha_respuesta_formateada(self, obj):
        if obj.fecha_respuesta:
            return obj.fecha_respuesta.strftime("%d-%m-%Y %H:%M")  # Formato: "01-03-2025 14:30"
        return ""
    fecha_respuesta_formateada.short_description = 'Fecha de Respuesta'

#Para enviar notificacion mediante correo
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change) 

        if not change:  # Solo si es un nuevo documento
            nro_registro = f'Nuevo documento registrado: {obj.nro_registro}'
            referencia = f'Se ha registrado un nuevo documento con el asunto: {obj.correspondencia.referencia}.\n\nContenido: {obj.correspondencia.referencia}'
            destinatarios = ['isabella172813@gmail.com']  # Lista de correos

            send_mail(
                nro_registro,
                referencia,
                'isatest172813@gmail.com',  # Remitente
                destinatarios,  # Lista de destinatarios
                fail_silently=False,
            )  
    
# Registra los demás modelos sin personalización
admin.site.register(Correspondencia)
admin.site.register(CorrespondenciaSaliente)
admin.site.register(TipoDocumento)

