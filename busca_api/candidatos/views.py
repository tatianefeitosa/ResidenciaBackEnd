# visualização de candidatos retornados pela API

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Candidato
from .models import Vaga
from .serializers import CandidatoCreateSerializer, CandidatoReadSerializer, CandidatoBatchSerializer

def resultados_view(request, vaga_id):
    vaga = Vaga.objects.get(id=vaga_id)
    candidatos = Candidato.objects.filter(vaga=vaga) 
    return render(request, 'candidatos/admin-resultado.html', {"vaga": vaga, "candidatos": candidatos})

def candidatos_page(request, vaga_id):
    vaga = Vaga.objects.get(id=vaga_id)
    candidatos = Candidato.objects.filter(vaga=vaga) 
    return render(request, 'candidatos/admin-candidatos.html', {"vaga": vaga, "candidatos": candidatos})

def candidato_detalhes_page(request, vaga_id, candidato_id):
    vaga = Vaga.objects.get(id=vaga_id)
    candidato = Candidato.objects.get(id=candidato_id)
    return render(request, 'candidatos/admin-candidato.html', {"vaga": vaga, "candidato": candidato})

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