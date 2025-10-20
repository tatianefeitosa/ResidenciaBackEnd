from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsAdministrador, IsSolicitante
from .models import Vaga

from .serializers import VagaSerializer, DecisaoVagaSerializer, VagaDetailSerializer

from .pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

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