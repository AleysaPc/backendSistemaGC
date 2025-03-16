from datetime import timezone
from django.contrib import admin
from django.http import HttpResponse
from docx import Document
from io import BytesIO
from .models import Correspondencia, CorrespondenciaEntrante, CorrespondenciaSaliente, TipoDocumento
from .models import FlujoAprobacion, DescargaDocumento


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
       return f"{remitente.nombre} - {remitente.apellido} - {institucion.nombre}"
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

@admin.register(CorrespondenciaSaliente)
class CorrespondenciaSalienteAdmin(admin.ModelAdmin):
    exclude = ('cite','fecha_recepcion', 'fecha_seguimiento',)
    readonly_fields = ('cite',)  # Marca 'cite' como solo lectura
    list_display = ('get_correspondencia_remitente', 'get_correspondencia_referencia', 'get_correspondencia_descripcion', 'get_correspondencia_prioridad', 'get_correspondencia_estado', 'get_correspondencia_personal_destinatario',)

    def get_correspondencia_remitente(self, obj):
        return obj.correspondencia.remitente
    get_correspondencia_remitente.short_description = 'Remitente'

    def get_correspondencia_referencia(self, obj):
        return obj.correspondencia.referencia
    get_correspondencia_referencia.short_description = 'Referencia'

    def get_correspondencia_descripcion(self, obj):
        return obj.correspondencia.descripcion
    get_correspondencia_descripcion.short_description = 'Descripción'

    def get_correspondencia_prioridad(self, obj):
        return obj.correspondencia.prioridad
    get_correspondencia_prioridad.short_description = 'Prioridad'

    def get_correspondencia_estado(self, obj):
        return obj.correspondencia.estado
    get_correspondencia_estado.short_description = 'Estado'

    def get_correspondencia_personal_destinatario(self, obj):
        return obj.correspondencia.personal_destinatario
    get_correspondencia_personal_destinatario.short_description = 'Personal destinatario'

    actions = ['generar_documento_word',]
    def generar_documento_word(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Solo puedes generar un documento a la vez.", level='error')
            return

        correspondencia_saliente = queryset.first()

        # Crear el archivo Word
        doc = Document()
        doc.add_paragraph(f"La Paz {correspondencia_saliente.fecha_envio.strftime('%Y-%m-%d')}")
        doc.add_paragraph(correspondencia_saliente.cite)
        doc.add_paragraph(correspondencia_saliente.correspondencia.remitente.nombre)
        doc.add_paragraph(correspondencia_saliente.correspondencia.remitente.apellido)
        doc.add_paragraph(correspondencia_saliente.correspondencia.remitente.cargo)
        doc.add_paragraph(str(correspondencia_saliente.correspondencia.remitente.institucion))    
        doc.add_paragraph(f"Ref.: {correspondencia_saliente.correspondencia.referencia}")
        doc.add_paragraph(correspondencia_saliente.correspondencia.descripcion)


        # Guardar el archivo en un buffer
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        # Devolver el archivo como respuesta
        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename=correspondencia_{correspondencia_saliente.cite}.docx'
        return response

    generar_documento_word.short_description = "Generar documento Word"
@admin.register(DescargaDocumento)
class DescargaDocumentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'documento', 'fecha_descarga')
    list_filter = ('usuario', 'documento')
    search_fields = ('usuario__nombre', 'documento__cite')
    readonly_fields = ('fecha_descarga',)

  



# Registra los demás modelos sin personalización

admin.site.register(Correspondencia)
admin.site.register(TipoDocumento)

