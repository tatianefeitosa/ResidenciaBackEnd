from django.urls import path
from .views import VagaDetailView, VagaListCreateView, VagasPendentesView, DecisaoVagaView

urlpatterns = [
    path('vagas/', VagaListCreateView.as_view(), name='vaga-list-create'), # solicitante cria e lista suas vagas, admin lista todas as vagas já criadas
    path('vagas/<int:pk>/', VagaDetailView.as_view(), name='vaga-detail'), # todos os detalhes da vaga (inclui requisitos)
    path('vagas/pendentes/', VagasPendentesView.as_view(), name='vagas-pendentes'), # lista vagas pendentes (somente admin)
    path('vagas/decisao/', DecisaoVagaView.as_view(), name='decisao-vaga'), # cria decisão de vaga, aprovar ou rejeitar + justificativa (somente admin)
]

# Spetacular (Swagger UI) para testing: http://127.0.0.1:8000/api/docs/
# use o access token do usuário que deseja testar as funcionalidades (gerado no login)

#http://127.0.0.1:8000/api/vagas/
#http://127.0.0.1:8000/api/vagas/1/
#http://127.0.0.1:8000/api/vagas/pendentes/
#http://127.0.0.1:8000/api/vagas/decisao/