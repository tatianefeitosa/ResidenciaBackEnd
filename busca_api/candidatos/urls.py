from django.urls import path
from .views import (
    CandidatoCreateView,
    CandidatoBatchCreateView,
    CandidatosPorVagaView,
    # adicione aqui suas outras views (List, Detail, Ranking etc.)
)

urlpatterns = [
    path('candidatos/', CandidatoCreateView.as_view(), name='candidato-create'),
    path('candidatos/lote/', CandidatoBatchCreateView.as_view(),name='candidato-batch-create'),
    path("resultados/", CandidatosPorVagaView.as_view(), name="candidatos-resultados"),
]
