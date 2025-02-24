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
    list_display = ('nro_registro', 'fecha_recepcion', 'fecha_respuesta', 'correspondencia')

# Registra los demás modelos sin personalización
admin.site.register(Correspondencia)
admin.site.register(CorrespondenciaSaliente)
admin.site.register(TipoDocumento)