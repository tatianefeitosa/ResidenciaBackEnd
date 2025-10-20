# visualização de candidatos retornados pela API

from rest_framework import generics, status
from rest_framework.response import Response
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