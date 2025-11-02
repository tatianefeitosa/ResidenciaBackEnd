from django.urls import path
from .views import solicitante_home

urlpatterns = [
    path('', solicitante_home, name='solicitante_home'),
]