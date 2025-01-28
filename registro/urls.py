from django.urls import path, include
from rest_framework import routers #genera la urls
from . import views

router = routers.DefaultRouter() #Configuracion de rutas para el API
router.register(r'registroRecibido', views.RegistroRecibidoView, 'Recibido') #register registra un viewset en el router

urlpatterns = [
    path('xyz/', include(router.urls)), #En el espacio " "estara registroRecibido

]

