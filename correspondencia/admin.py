from django.contrib import admin
from plantilla.utils import generar_documento_word
from .models import CorrespondenciaEntrante, CorrespondenciaSaliente, TipoDocumento
from .models import TipoDocumentoInterno, CorrespondenciaInterna


# Configuración personalizada para CorrespondenciaEntrante
@admin.register(CorrespondenciaEntrante)
class CorrespondenciaEntranteAdmin(admin.ModelAdmin):
    # Excluye el campo nro_registro del formulario
    exclude = ('nro_registro','estado',)

    # Si deseas mostrar el campo como de solo lectura, agrégalo a readonly_fields
    readonly_fields = ('nro_registro',)

    # Campos que se mostrarán en la lista de registros en el admin
    list_display = ('nro_registro', 'fecha_recepcion_formateada', 'fecha_respuesta_formateada', 'mostrar_referencia', 'mostrar_remitente')

    # Metodo para mostrar la referencia
    def mostrar_referencia(self, obj):
        # Acceder al campo 'referencia' del modelo relacionado 'Correspondencia'
        return obj.referencia
    mostrar_referencia.short_description = 'Referencia'

    #Metodo para mostrar remitente
    def mostrar_remitente(self, obj):
       remitente = obj.remitente
       institucion = remitente.institucion 
       return f"{remitente.apellido} - {institucion.nombre_institucion}"
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
    list_display = ('cite', 'referencia', 'mostrar_remitente', 'fecha_envio', 'estado')
    fields = ('cite', 'fecha_envio', 'remitente', 'referencia', 'descripcion', 
              'prioridad', 'estado', 'personal_destinatario', 'archivo_word')
    readonly_fields = ('cite',)

    def mostrar_remitente(self, obj):
       remitente = obj.remitente
       institucion = remitente.institucion 
       return f"{remitente.apellido} - {institucion.nombre}"
    mostrar_remitente.short_description = 'Remitente'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "remitente":
            kwargs["label"] = "Destinatario"  # Cambiar el nombre en la interfaz
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_fields(self, request, obj=None):
        base_fields = super().get_fields(request, obj)

        # Si la correspondencia está aprobada, se agregan campos adicionales y se excluye 'archivo_word'
        if obj and obj.estado == 'aprobado':
            return tuple(field for field in base_fields if field != 'archivo_word') + (
                'fecha_recepcion', 'fecha_seguimiento', 'paginas', 'documento'
            )

        return base_fields

           
    actions = ['accion_generar_documento_word']

    def accion_generar_documento_word(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Solo puedes generar un documento a la vez.", level='error')
            return
        correspondencia_saliente = queryset.first()
        return generar_documento_word(correspondencia_saliente)  # Llamamos a la función importada
    accion_generar_documento_word.short_description = "Generar documento Word"


@admin.register(TipoDocumentoInterno)
class TipoDocumentoInternoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(CorrespondenciaInterna)
class CorrespondenciaInternaAdmin(admin.ModelAdmin):
    list_display = ('cite', 'tipo', 'numero', 'gestion', 'fecha_creacion', 'personal_destinatario')
    readonly_fields = ('numero', 'gestion', 'cite')  # No permitir modificar estos campos
    ordering = ('-gestion', '-numero')  # Ordenar de manera descendente




# Registra los demás modelos sin personalización

admin.site.register(TipoDocumento)

