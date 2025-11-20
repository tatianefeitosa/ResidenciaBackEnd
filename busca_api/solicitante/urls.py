from django.urls import path
from .views import solicitante_home
from .views import solicitar_vaga

urlpatterns = [
    path('', solicitante_home, name='solicitante_home'),
    path('solicitar-vaga/', solicitar_vaga, name='solicitar_vaga'),
]