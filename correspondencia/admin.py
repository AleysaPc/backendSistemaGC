from django.contrib import admin
from .models import Correspondencia, CorrespondenciaEntrante, CorrespondenciaSaliente, TipoDocumento


admin.site.register(Correspondencia)
admin.site.register(CorrespondenciaEntrante)
admin.site.register(CorrespondenciaSaliente)
admin.site.register(TipoDocumento)
