from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsAdministrador, IsSolicitante
from .models import Vaga

from .serializers import VagaSerializer, DecisaoVagaSerializer, VagaDetailSerializer

from .pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
#from vagas.tasks import scraping_task

# Listar e criar vagas
class VagaListCreateView(generics.ListCreateAPIView):
    serializer_class = VagaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination # paginação
    
    ordering_fields = ['id', 'data_solicitacao'] # permite filtrar por id e data_solicitacao
    ordering = ['-id']  # padrão: mais recentes primeiro

   

    #admin vê todas a vagas aprovadas, solicitante vê as vagas que criou
    def get_queryset(self):
        user = self.request.user
        if user.tipo == 'administrador':
            return Vaga.objects.filter(status='Aprovada').order_by(*self.ordering)
        elif user.tipo == 'solicitante':
            return Vaga.objects.filter(solicitante=user).order_by(*self.ordering)
        return Vaga.objects.none()
    
    # impedir que admin crie vaga
    def perform_create(self, serializer):
        user = self.request.user
        if user.tipo != 'solicitante':
            raise PermissionDenied("Somente solicitantes podem criar vagas.")
        serializer.save(solicitante=user, status='Pendente')



# Listar vagas pendentes (admin)
class VagasPendentesView(generics.ListAPIView):
    serializer_class = VagaSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]
    pagination_class = CustomPageNumberPagination # paginação
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['prioridade']  # permite filtrar por prioridade
    ordering_fields = ['id', 'data_solicitacao'] # permite filtrar por id e data_solicitacao
    ordering = ['id']  # padrão: mais antigas primeiro

    def get_queryset(self):
        return Vaga.objects.filter(status='Pendente').order_by(*self.ordering)



# Criar decisão de vaga (admin)
class DecisaoVagaView(generics.CreateAPIView):
    serializer_class = DecisaoVagaSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]

    def perform_create(self, serializer):
        serializer.save(administrador=self.request.user)


# Detalhes da vaga (inclui requisitos)
class VagaDetailView(generics.RetrieveAPIView):
    serializer_class = VagaDetailSerializer
    permission_classes = [IsAuthenticated, IsSolicitante | IsAdministrador]

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Vaga.objects
            .select_related('solicitante')
            .prefetch_related(
                'decisoes',
                'vagahabilidadetecnica_set__habilidade',
                'vagahabilidadeinterpessoal_set__habilidade',
                'vagadiploma_set__diploma',
                'vagacertificacao_set__certificacao',
                'vagaidioma_set__idioma',
                'vagaempresa_set__empresa',
                'vagalocalizacao_set__localizacao'
            )
        )

        # solicitante vê apenas detalhes das suas vagas
        if getattr(user, 'tipo', None) == 'solicitante':
            return queryset.filter(solicitante=user)

        # administrador vê apenas detalhes das vagas aprovadas
        if getattr(user, 'tipo', None) == 'administrador':
            return queryset.filter(status='Aprovada')

        return Vaga.objects.none()


'''class IniciarScrapingGithub(APIView):
    """
    Endpoint responsável por disparar a task Celery que faz o scraping.
    """

    @extend_schema(
        summary="Inicia o scraping no GitHub para uma vaga",
        request={
        "application/json": {
            "type": "object",
            "properties": {"vaga_id": {"type": "integer"}},
            "required": ["vaga_id"]
            }
        },
        responses={200: dict, 404: dict},
    )
    def post(self, request):
        vaga_id = request.data.get("vaga_id")

        if not vaga_id:
            return Response(
                {"erro": "O campo 'vaga_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            vaga = Vaga.objects.get(id=vaga_id)
        except Vaga.DoesNotExist:
            return Response(
                {"erro": f"Vaga com id={vaga_id} não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # dispara task Celery
        scraping_task.delay(vaga_id)

        return Response(
            {
                "mensagem": "Scraping iniciado com sucesso.",
                "vaga_id": vaga_id,
                "status": "PROCESSING",
            },
            status=status.HTTP_200_OK,
        )
'''