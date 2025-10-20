from rest_framework import serializers
from .models import (
    Vaga, DecisaoVaga,
    HabilidadeTecnica, HabilidadeInterpessoal, Diploma,
    Certificacao, Idioma, Empresa, Localizacao, VagaHabilidadeTecnica, VagaHabilidadeInterpessoal,
    VagaDiploma, VagaCertificacao, VagaIdioma, VagaEmpresa, VagaLocalizacao
)

# Serializers básicos (requisitos)

class HabilidadeTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabilidadeTecnica
        fields = ['id', 'nome']


class HabilidadeInterpessoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabilidadeInterpessoal
        fields = ['id', 'nome']


class DiplomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diploma
        fields = ['id', 'tipo', 'area']


class CertificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificacao
        fields = ['id', 'nome']


class IdiomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idioma
        fields = ['id', 'nome', 'nivel']


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nome', 'nivel']


class LocalizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizacao
        fields = ['id', 'pais', 'estado', 'cidade']


# Serializers intermediários (N:N)

class VagaHabilidadeTecnicaSerializer(serializers.ModelSerializer):
    habilidade = HabilidadeTecnicaSerializer()
    class Meta:
        model = VagaHabilidadeTecnica
        fields = ['habilidade']

class VagaHabilidadeInterpessoalSerializer(serializers.ModelSerializer):
    habilidade = HabilidadeInterpessoalSerializer()
    class Meta:
        model = VagaHabilidadeInterpessoal
        fields = ['habilidade']

class VagaDiplomaSerializer(serializers.ModelSerializer):
    diploma = DiplomaSerializer()
    class Meta:
        model = VagaDiploma
        fields = ['diploma']

class VagaCertificacaoSerializer(serializers.ModelSerializer):
    certificacao = CertificacaoSerializer()
    class Meta:
        model = VagaCertificacao
        fields = ['certificacao']

class VagaIdiomaSerializer(serializers.ModelSerializer):
    idioma = IdiomaSerializer()
    class Meta:
        model = VagaIdioma
        fields = ['idioma']

class VagaEmpresaSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()
    class Meta:
        model = VagaEmpresa
        fields = ['empresa']

class VagaLocalizacaoSerializer(serializers.ModelSerializer):
    localizacao = LocalizacaoSerializer()
    class Meta:
        model = VagaLocalizacao
        fields = ['localizacao']

# Serializers principais

class VagaSerializer(serializers.ModelSerializer):
    habilidades_tecnicas = HabilidadeTecnicaSerializer(many=True, required=False)
    habilidades_interpessoais = HabilidadeInterpessoalSerializer(many=True, required=False)
    diplomas = DiplomaSerializer(many=True, required=False)
    certificacoes = CertificacaoSerializer(many=True, required=False)
    idiomas = IdiomaSerializer(many=True, required=False)
    empresas = EmpresaSerializer(many=True, required=False)
    localizacoes = LocalizacaoSerializer(many=True, required=False)

    solicitante = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vaga
        fields = [
            'id', 'nome_cargo', 'modalidade', 'tipo_contrato', 'quantidade',
            'prioridade', 'observacao', 'data_solicitacao', 'solicitante',
            'habilidades_tecnicas', 'habilidades_interpessoais', 'diplomas',
            'certificacoes', 'idiomas', 'empresas', 'localizacoes', 'status'
        ]
        reade_only_fields = ['status', 'solicitante']

    def create(self, validated_data):
        nested_fields = {
            'habilidades_tecnicas': HabilidadeTecnica,
            'habilidades_interpessoais': HabilidadeInterpessoal,
            'diplomas': Diploma,
            'certificacoes': Certificacao,
            'idiomas': Idioma,
            'empresas': Empresa,
            'localizacoes': Localizacao,
        }

        # Extrair dados nested
        nested_data = {}
        for key in nested_fields.keys():
            nested_data[key] = validated_data.pop(key, [])

        # Criar vaga principal
        vaga = Vaga.objects.create(**validated_data)

        # Criar objetos aninhados e relacionamentos N:N
        for key, Model in nested_fields.items():
            for item in nested_data[key]:
                obj = Model.objects.create(**item)
                # Criar relação N:N automática
                if key == 'habilidades_tecnicas':
                    VagaHabilidadeTecnica.objects.create(vaga=vaga, habilidade=obj)
                elif key == 'habilidades_interpessoais':
                    VagaHabilidadeInterpessoal.objects.create(vaga=vaga, habilidade=obj)
                elif key == 'diplomas':
                    VagaDiploma.objects.create(vaga=vaga, diploma=obj)
                elif key == 'certificacoes':
                    VagaCertificacao.objects.create(vaga=vaga, certificacao=obj)
                elif key == 'idiomas':
                    VagaIdioma.objects.create(vaga=vaga, idioma=obj)
                elif key == 'empresas':
                    VagaEmpresa.objects.create(vaga=vaga, empresa=obj)
                elif key == 'localizacoes':
                    VagaLocalizacao.objects.create(vaga=vaga, localizacao=obj)

        return vaga




class DecisaoVagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisaoVaga
        fields = ['id', 'vaga', 'administrador', 'status', 'justificativa', 'data_decisao']
        read_only_fields = ['administrador', 'data_decisao']




class VagaCreateSerializer(serializers.ModelSerializer):
    """criação de vaga pelo solicitante"""
    class Meta:
        model = Vaga
        fields = [
            'nome_cargo', 'modalidade', 'tipo_contrato',
            'quantidade', 'prioridade', 'observacao'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        return Vaga.objects.create(solicitante=user, **validated_data)


class VagaDetailSerializer(serializers.ModelSerializer):
    habilidades_tecnicas = serializers.SerializerMethodField()
    habilidades_interpessoais = serializers.SerializerMethodField()
    diplomas = serializers.SerializerMethodField()
    certificacoes = serializers.SerializerMethodField()
    idiomas = serializers.SerializerMethodField()
    empresas = serializers.SerializerMethodField()
    localizacoes = serializers.SerializerMethodField()

    solicitante = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vaga
        fields = [
            'id', 'nome_cargo', 'modalidade', 'tipo_contrato', 'quantidade',
            'prioridade', 'observacao', 'data_solicitacao', 'solicitante',
            'habilidades_tecnicas', 'habilidades_interpessoais', 'diplomas',
            'certificacoes', 'idiomas', 'empresas', 'localizacoes', 'status'
        ]
        read_only_fields = ['status', 'solicitante']

    def get_habilidades_tecnicas(self, obj):
        qs = VagaHabilidadeTecnica.objects.filter(vaga=obj).select_related('habilidade')
        return HabilidadeTecnicaSerializer([r.habilidade for r in qs], many=True).data

    def get_habilidades_interpessoais(self, obj):
        qs = VagaHabilidadeInterpessoal.objects.filter(vaga=obj).select_related('habilidade')
        return HabilidadeInterpessoalSerializer([r.habilidade for r in qs], many=True).data

    def get_diplomas(self, obj):
        qs = VagaDiploma.objects.filter(vaga=obj).select_related('diploma')
        return DiplomaSerializer([r.diploma for r in qs], many=True).data

    def get_certificacoes(self, obj):
        qs = VagaCertificacao.objects.filter(vaga=obj).select_related('certificacao')
        return CertificacaoSerializer([r.certificacao for r in qs], many=True).data

    def get_idiomas(self, obj):
        qs = VagaIdioma.objects.filter(vaga=obj).select_related('idioma')
        return IdiomaSerializer([r.idioma for r in qs], many=True).data

    def get_empresas(self, obj):
        qs = VagaEmpresa.objects.filter(vaga=obj).select_related('empresa')
        return EmpresaSerializer([r.empresa for r in qs], many=True).data

    def get_localizacoes(self, obj):
        qs = VagaLocalizacao.objects.filter(vaga=obj).select_related('localizacao')
        return LocalizacaoSerializer([r.localizacao for r in qs], many=True).data
