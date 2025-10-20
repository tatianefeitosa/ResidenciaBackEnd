from django.db import models
from usuarios.models import Usuario # Importa o modelo de usuário

# Choices equivalentes aos DOMAINS do PostegreSQL
class ModalidadeChoices(models.TextChoices):
    PRESENCIAL = 'Presencial', 'Presencial'
    DISTANCIA = 'À distância', 'À distância'
    HIBRIDO = 'Híbrido', 'Híbrido'


class ContratoChoices(models.TextChoices):
    INDETERMINADO = 'Prazo indeterminado', 'Prazo indeterminado'
    DETERMINADO = 'Prazo determinado', 'Prazo determinado'
    EXPERIENCIA = 'Experiência', 'Experiência'
    TEMPORARIO = 'Temporário', 'Temporário'
    INTERMITENTE = 'Intermitente', 'Intermitente'
    ESTAGIO = 'Estágio', 'Estágio'


class PrioridadeChoices(models.TextChoices):
    BAIXA = 'Baixa', 'Baixa'
    MEDIA = 'Média', 'Média'
    ALTA = 'Alta', 'Alta'


class StatusChoices(models.TextChoices):
    PENDENTE = 'Pendente', 'Pendente'
    APROVADA = 'Aprovada', 'Aprovada'
    REJEITADA = 'Rejeitada', 'Rejeitada'


class DiplomaTipoChoices(models.TextChoices):
    BACHARELADO = 'Bacharelado', 'Bacharelado'
    LICENCIATURA = 'Licenciatura', 'Licenciatura'
    TECNOLOGO = 'Tecnólogo', 'Tecnólogo'
    MESTRADO = 'Mestrado', 'Mestrado'
    DOUTORADO = 'Doutorado', 'Doutorado'


class NivelChoices(models.TextChoices):
    BASICO = 'Básico', 'Básico'
    INTERMEDIARIO = 'Intermediário', 'Intermediário'
    AVANCADO = 'Avançado', 'Avançado'
    FLUENTE = 'Fluente', 'Fluente'


class SenioridadeChoices(models.TextChoices):
    JUNIOR = 'Júnior', 'Júnior'
    PLENO = 'Pleno', 'Pleno'
    SENIOR = 'Sênior', 'Sênior'


# TABELAS PRINCIPAIS

class Vaga(models.Model):
    nome_cargo = models.CharField(max_length=100)
    modalidade = models.CharField(max_length=20, choices=ModalidadeChoices.choices)
    tipo_contrato = models.CharField(max_length=30, choices=ContratoChoices.choices)
    quantidade = models.PositiveIntegerField(default=1)
    prioridade = models.CharField(max_length=10, choices=PrioridadeChoices.choices)
    observacao = models.TextField(blank=True, null=True)
    data_solicitacao = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDENTE)

    # FK para solicitante
    solicitante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='vagas_solicitadas'
    )

    def __str__(self):
        return f"{self.nome_cargo} ({self.status})"


class DecisaoVaga(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='decisoes')
    administrador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='vagas_analisadas'
    )
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    justificativa = models.TextField(blank=True, null=True)
    data_decisao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vaga.nome_cargo} - {self.status}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vaga.status = self.status
        self.vaga.save(update_fields=['status'])


# TABELAS DE REQUISITOS

class HabilidadeTecnica(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class HabilidadeInterpessoal(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Diploma(models.Model):
    tipo = models.CharField(max_length=20, choices=DiplomaTipoChoices.choices)
    area = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tipo} em {self.area}"


class Certificacao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Idioma(models.Model):
    nome = models.CharField(max_length=50)
    nivel = models.CharField(max_length=15, choices=NivelChoices.choices)

    def __str__(self):
        return f"{self.nome} ({self.nivel})"


class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    nivel = models.CharField(max_length=10, choices=SenioridadeChoices.choices)

    def __str__(self):
        return f"{self.nome} ({self.nivel})"


class Localizacao(models.Model):
    pais = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.cidade}, {self.estado}, {self.pais}"


# RELACIONAMENTOS N:N

class VagaHabilidadeTecnica(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    habilidade = models.ForeignKey(HabilidadeTecnica, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vaga', 'habilidade')


class VagaHabilidadeInterpessoal(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    habilidade = models.ForeignKey(HabilidadeInterpessoal, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vaga', 'habilidade')


class VagaDiploma(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vaga', 'diploma')


class VagaCertificacao(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    certificacao = models.ForeignKey(Certificacao, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vaga', 'certificacao')


class VagaIdioma(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vaga', 'idioma')


class VagaEmpresa(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vaga', 'empresa')


class VagaLocalizacao(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vaga', 'localizacao')

