"""
URL configuration for gestion_correspondencia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from email_service.api.views import EmailAPIView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/correspondencia/',include(('correspondencia.urls','correspondencia'), namespace='correspondencia')),
    path('send-email', EmailAPIView.as_view(), name='send-email'),
    path('api/v1/documento/',include(('documento.urls','documento'), namespace='documento')),

]

# Solo en desarrollo: Servir archivos de MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)