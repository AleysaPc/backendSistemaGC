from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteView, InstitucionView

# Crear el router
router = DefaultRouter()

# Registrar las rutas si las vistas son ViewSets
router.register(r'cliente', ClienteView)
router.register(r'institucion', InstitucionView)

urlpatterns = [
    path('', include(router.urls)),  # Incluir las rutas generadas por el router
]