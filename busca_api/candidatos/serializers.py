from rest_framework import serializers
from django.db.models import JSONField

from .models import (
    Candidato, CandidatoEmail, CandidatoTelefone, CandidatoFonteBusca,
    CandidatoHabilidadeTecnica, CandidatoHabilidadeInterpessoal,
    CandidatoDiploma, CandidatoCertificacao, CandidatoIdioma,
    CandidatoEmpresa, CandidatoLocalizacao, FonteBusca
)
from vagas.models import (
    HabilidadeTecnica, HabilidadeInterpessoal, Diploma,
    Certificacao, Idioma, Empresa, Localizacao, Vaga
)



# Serializers básicos (requisitos retornados do candidato)

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


class CandidatoHabilidadeTecnicaSerializer(serializers.ModelSerializer):
    habilidade = HabilidadeTecnicaSerializer()
    class Meta:
        model = CandidatoHabilidadeTecnica
        fields = ['habilidade']

class CandidatoHabilidadeInterpessoalSerializer(serializers.ModelSerializer):
    habilidade = HabilidadeInterpessoalSerializer()
    class Meta:
        model = CandidatoHabilidadeInterpessoal
        fields = ['habilidade']

class CandidatoDiplomaSerializer(serializers.ModelSerializer):
    diploma = DiplomaSerializer()
    class Meta:
        model = CandidatoDiploma
        fields = ['diploma']

class CandidatoCertificacaoSerializer(serializers.ModelSerializer):
    certificacao = CertificacaoSerializer()
    class Meta:
        model = CandidatoCertificacao
        fields = ['certificacao']

class CandidatoIdiomaSerializer(serializers.ModelSerializer):
    idioma = IdiomaSerializer()
    class Meta:
        model = CandidatoIdioma
        fields = ['idioma']

class CandidatoEmpresaSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()
    class Meta:
        model = CandidatoEmpresa
        fields = ['empresa']

class CandidatoLocalizacaoSerializer(serializers.ModelSerializer):
    localizacao = LocalizacaoSerializer()
    class Meta:
        model = CandidatoLocalizacao
        fields = ['localizacao']



# Serializers intermediários candidato (1:N)

class FonteBuscaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FonteBusca
        fields = ['nome_site', 'url_perfil']


class CandidatoEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatoEmail
        fields = ['email']


class CandidatoTelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatoTelefone
        fields = ['telefone']

class CandidatoFonteBuscaSerializer(serializers.ModelSerializer):
    fonte = FonteBuscaSerializer()

    class Meta:
        model = CandidatoFonteBusca
        fields = ['fonte']


# Serializer para retornar dados completos ao front-end

class CandidatoReadSerializer(serializers.ModelSerializer):
    emails = CandidatoEmailSerializer(many=True, read_only=True)
    telefones = CandidatoTelefoneSerializer(many=True, read_only=True)
    fontes_busca = CandidatoFonteBuscaSerializer(many=True, read_only=True)
    habilidades_tecnicas = CandidatoHabilidadeTecnicaSerializer(many=True, read_only=True)
    habilidades_interpessoais = CandidatoHabilidadeInterpessoalSerializer(many=True, read_only=True)
    diplomas = CandidatoDiplomaSerializer(many=True, read_only=True)
    certificacoes = CandidatoCertificacaoSerializer(many=True, read_only=True)
    idiomas = CandidatoIdiomaSerializer(many=True, read_only=True)
    empresas = CandidatoEmpresaSerializer(many=True, read_only=True)
    localizacoes = CandidatoLocalizacaoSerializer(many=True, read_only=True)

    # Novos campos GitHub
    bio = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    location = serializers.CharField(read_only=True)
    repos = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = Candidato
        fields = [
            'id', 'nome_candidato', 'data_nascimento', 'resumo_profissional',
            'compatibilidade', 'vaga', 'emails', 'telefones', 'fontes_busca',
            'habilidades_tecnicas', 'habilidades_interpessoais',
            'diplomas', 'certificacoes', 'idiomas', 'empresas', 'localizacoes',
            'bio', 'company', 'location', 'repos'
        ]



# Serializer para criação de candidato

class CandidatoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para receber os dados do scraping (ou criação manual)
    com estrutura aninhada e campos compostos.
    """
    source_id_hash = serializers.CharField(required=False)
    raw_result = serializers.JSONField(required=False)

    emails = CandidatoEmailSerializer(many=True, required=False, write_only=True)
    telefones = CandidatoTelefoneSerializer(many=True, required=False, write_only=True)
    fontes_busca = CandidatoFonteBuscaSerializer(many=True, required=False, write_only=True)

    habilidades_tecnicas = HabilidadeTecnicaSerializer(many=True, required=False, write_only=True)
    habilidades_interpessoais = HabilidadeInterpessoalSerializer(many=True, required=False, write_only=True)
    diplomas = DiplomaSerializer(many=True, required=False, write_only=True)
    certificacoes = CertificacaoSerializer(many=True, required=False, write_only=True)
    idiomas = IdiomaSerializer(many=True, required=False, write_only=True)
    empresas = EmpresaSerializer(many=True, required=False, write_only=True)
    localizacoes = LocalizacaoSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Candidato
        fields = [
            'nome_candidato', 'data_nascimento', 'resumo_profissional', 'vaga',
            'emails', 'telefones', 'fontes_busca',
            'habilidades_tecnicas', 'habilidades_interpessoais',
            'diplomas', 'certificacoes', 'idiomas', 'empresas', 'localizacoes', 'source_id_hash', 'raw_result'
        ]

    def create(self, validated_data):
        """
        Criação de candidato e seus relacionamentos aninhados.
        Permite receber dicionários completos (ex: {"nome": "Python"}) e campos compostos.
        """
        # Extrai dados aninhados
        emails_data = validated_data.pop('emails', [])
        telefones_data = validated_data.pop('telefones', [])
        fontes_data = validated_data.pop('fontes_busca', [])

        habilidades_tecnicas_data = validated_data.pop('habilidades_tecnicas', [])
        habilidades_interpessoais_data = validated_data.pop('habilidades_interpessoais', [])
        diplomas_data = validated_data.pop('diplomas', [])
        certificacoes_data = validated_data.pop('certificacoes', [])
        idiomas_data = validated_data.pop('idiomas', [])
        empresas_data = validated_data.pop('empresas', [])
        localizacoes_data = validated_data.pop('localizacoes', [])

        candidato = Candidato.objects.create(**validated_data)

        # ---- Criação simples 1:N
        for email in emails_data:
            CandidatoEmail.objects.create(candidato=candidato, **email)
        for telefone in telefones_data:
            CandidatoTelefone.objects.create(candidato=candidato, **telefone)
        for fonte_data in fontes_data:
            fonte_info = fonte_data.get('fonte', fonte_data)
            fonte_obj, _ = FonteBusca.objects.get_or_create(**fonte_info)
            CandidatoFonteBusca.objects.create(candidato=candidato, fonte=fonte_obj)



        # ---- Helper para N:N e tabelas intermediárias
        def get_or_create_related(model, data, unique_fields):
            """
            Retorna (obj, created) usando filtros dinâmicos para campos únicos.
            """
         # Cria dicionário de busca com base nos campos únicos
            lookup = {field: data.get(field) for field in unique_fields if data.get(field) is not None}

            # Primeiro tenta encontrar exatamente 1 objeto
            try:
                obj = model.objects.get(**lookup)
            except model.DoesNotExist:
                # Não existe → cria novo
                obj = model.objects.create(**data)
            except model.MultipleObjectsReturned:
                # Existe mais de um → usa o primeiro
                obj = model.objects.filter(**lookup).first()

            return obj
        

        for item in habilidades_tecnicas_data:
            obj = get_or_create_related(HabilidadeTecnica, item, ['nome'])
            CandidatoHabilidadeTecnica.objects.get_or_create(candidato=candidato, habilidade=obj)

        for item in habilidades_interpessoais_data:
            obj = get_or_create_related(HabilidadeInterpessoal, item, ['nome'])
            CandidatoHabilidadeInterpessoal.objects.get_or_create(candidato=candidato, habilidade=obj)

        for item in diplomas_data:
            obj = get_or_create_related(Diploma, item, ['tipo', 'area'])
            CandidatoDiploma.objects.get_or_create(candidato=candidato, diploma=obj)

        for item in certificacoes_data:
            obj = get_or_create_related(Certificacao, item, ['nome'])
            CandidatoCertificacao.objects.get_or_create(candidato=candidato, certificacao=obj)

        for item in idiomas_data:
            obj = get_or_create_related(Idioma, item, ['nome', 'nivel'])
            CandidatoIdioma.objects.get_or_create(candidato=candidato, idioma=obj)

        for item in empresas_data:
            obj = get_or_create_related(Empresa, item, ['nome', 'nivel'])
            CandidatoEmpresa.objects.get_or_create(candidato=candidato, empresa=obj)

        for item in localizacoes_data:
            obj = get_or_create_related(Localizacao, item, ['pais', 'estado', 'cidade'])
            CandidatoLocalizacao.objects.get_or_create(candidato=candidato, localizacao=obj)

        return candidato

    def to_representation(self, instance):
        # Use o serializer de leitura para saída consistente
        return CandidatoReadSerializer(instance).data
    

# Serializer para criação de vários candidatos de uma vez(receber lista de candidatos do scraping)

class CandidatoBatchSerializer(serializers.Serializer):
    vaga = serializers.PrimaryKeyRelatedField(queryset=Vaga.objects.all())
    candidatos = CandidatoCreateSerializer(many=True)

    def create(self, validated_data):
        vaga = validated_data['vaga']
        candidatos_data = validated_data['candidatos']
        created_candidatos = []

        for candidato_data in candidatos_data:
            candidato_data['vaga'] = vaga

            serializer = CandidatoCreateSerializer(data=candidato_data)
            serializer.is_valid(raise_exception=True)
            candidato = serializer.save()
            created_candidatos.append(candidato)

        return created_candidatos
    
    def to_representation(self, instance):
        # Caso queira retornar todos os candidatos criados já serializados
        return CandidatoCreateSerializer(instance, many=True).data
