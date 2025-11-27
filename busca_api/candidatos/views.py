# visualização de candidatos retornados pela API

from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Candidato
from .serializers import CandidatoCreateSerializer, CandidatoReadSerializer, CandidatoBatchSerializer


class CandidatoCreateView(generics.CreateAPIView):
    queryset = Candidato.objects.all()
    serializer_class = CandidatoCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        candidato = serializer.save()
        return Response(CandidatoReadSerializer(candidato).data, status=status.HTTP_201_CREATED)


class CandidatoBatchCreateView(generics.CreateAPIView):
    queryset = Candidato.objects.all()
    serializer_class = CandidatoBatchSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        candidatos = serializer.save()
        return Response(CandidatoReadSerializer(candidatos, many=True).data, status=status.HTTP_201_CREATED)



@extend_schema(
    parameters=[
        OpenApiParameter(
            name="vaga_id",
            description="ID da vaga para filtrar os candidatos resultantes do scraping",
            required=True,
            type=int,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="top_n",
            description="Número máximo de candidatos a retornar",
            required=False,
            type=int,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={200: CandidatoReadSerializer(many=True)},
)
class CandidatosPorVagaView(generics.ListAPIView):
    serializer_class = CandidatoReadSerializer

    def get_queryset(self):
        vaga_id = self.request.query_params.get("vaga_id")
        if not vaga_id:
            return Candidato.objects.none()
        return Candidato.objects.filter(vaga_id=vaga_id).order_by('-compatibilidade')

    def list(self, request, *args, **kwargs):
        vaga_id = request.query_params.get("vaga_id")
        top_n = int(request.query_params.get("top_n", 5))

        if not vaga_id:
            return Response({"detail": "Parâmetro vaga_id é obrigatório."}, status=400)

        queryset = self.get_queryset()[:top_n]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)