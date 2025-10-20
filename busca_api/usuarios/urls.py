from django.urls import path

from .views import RegisterView, LoginView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    #path('', views.test_usuario, name='test_usuario'),  # Exemplo de endpoint de teste


]

# teste para register: http://127.0.0.1:8000/api/usuarios/register/
# teste para login: http://127.0.0.1:8000/api/usuarios/login/