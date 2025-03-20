from django.contrib import admin
from .models import Plantilla

# Register your models here.
@admin.register(Plantilla)
class PlantillaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contenido')

