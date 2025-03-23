from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PlantillaView

# Crear el router
router = DefaultRouter()

# Registrar las rutas si las vistas son ViewSets
router.register(r'plantilla', PlantillaView)

urlpatterns = [
    path('', include(router.urls)),  # Incluir las rutas generadas por el router
]