"""
URL configuration for busca_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def index(request):
    return render(request, "index.html")  # front principal

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", index),

    # usuários
    path('api/usuarios/', include('usuarios.urls')),

    # solicitante
    path('solicitante/', include('solicitante.urls')),

    # vagas
    path('api/', include('vagas.urls')),

    # administração
    path('administracao/', include('administracao.urls')),

    # candidatos / resultados
    path("candidatos/", include("candidatos.urls")),
    
    # endpoints do drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
