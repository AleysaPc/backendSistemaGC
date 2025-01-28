from django.contrib import admin

from registro.models import DatosRemitente, Directorio, RegistroRecibido

# Register your models here.
admin.site.register(DatosRemitente)
admin.site.register(Directorio)
admin.site.register(RegistroRecibido)
