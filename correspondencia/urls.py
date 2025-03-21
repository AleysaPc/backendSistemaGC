from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CorrespondenciaView, CorrespondenciaEntranteView, CorrespondenciaSalienteView

# Crear el router
router = DefaultRouter()

# Registrar las rutas si las vistas son ViewSets
router.register(r'correspondencia', CorrespondenciaView)
router.register(r'correspondenciaEntrante', CorrespondenciaEntranteView)
router.register(r'correspondenciaSaliente', CorrespondenciaSalienteView)

urlpatterns = [
    path('', include(router.urls)),  # Incluir las rutas generadas por el router
]
