from django.urls import path
from .views import admin_inicio
from .views import admin_vagas

urlpatterns = [
    path('', admin_inicio, name='admin_inicio'),
    path('admin_vagas/', admin_vagas, name='admin_vagas'),
]