from django.contrib import admin
from .models import Correspondencia, CorrespondenciaEntrante, CorrespondenciaSaliente, TipoDocumento

# Configuración personalizada para CorrespondenciaEntrante
@admin.register(CorrespondenciaEntrante)
class CorrespondenciaEntranteAdmin(admin.ModelAdmin):
    # Excluye el campo nro_registro del formulario
    exclude = ('nro_registro',)

    # Si deseas mostrar el campo como de solo lectura, agrégalo a readonly_fields
    readonly_fields = ('nro_registro',)

    # Campos que se mostrarán en la lista de registros en el admin
    list_display = ('nro_registro', 'fecha_recepcion_formateada', 'fecha_respuesta_formateada', 'correspondencia')

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
    
# Registra los demás modelos sin personalización
admin.site.register(Correspondencia)
admin.site.register(CorrespondenciaSaliente)
admin.site.register(TipoDocumento)

