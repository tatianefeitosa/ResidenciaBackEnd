from django.urls import path
from .views import (
    CandidatoCreateView,
    CandidatoBatchCreateView,
    resultados_view,
    candidatos_page,
    candidato_detalhes_page

    # adicione aqui suas outras views (List, Detail, Ranking etc.)
)

urlpatterns = [
    path('resultado/<int:vaga_id>/', resultados_view, name='resultado-vaga'),
    path('candidatos/<int:vaga_id>/', candidatos_page, name='candidatos-vaga'),
    path('candidatos/<int:vaga_id>/<int:candidato_id>/', candidato_detalhes_page, name='candidato-detalhes'),
    path('candidatos/', CandidatoCreateView.as_view(), name='candidato-create'),
    path('candidatos/lote/', CandidatoBatchCreateView.as_view(),name='candidato-batch-create'),
    path("resultados/", CandidatosPorVagaView.as_view(), name="candidatos-resultados"),
]
