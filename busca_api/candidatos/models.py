from django.db import models
from vagas.models import HabilidadeTecnica, HabilidadeInterpessoal, Diploma, Certificacao, Idioma, Empresa, Localizacao, Vaga


# Fonte onde o candidato foi encontrado (Github, Lattes)
class FonteBusca(models.Model):
    nome_site = models.CharField(max_length=100)
    url_perfil = models.URLField(blank=True, null=True) # link direto para o perfil do candidato

    def __str__(self):
        return self.nome_site
    

# Candidato retornado pelo scraping
class Candidato(models.Model):
    nome_candidato = models.CharField(max_length=100)
    data_nascimento = models.DateField(blank=True, null=True)
    resumo_profissional = models.TextField(blank=True, null=True) # vai ser gerado
    compatibilidade = models.FloatField(default=0.0)  # porcentagem 0–100%

    # chave estrangeira de vaga
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidatos')

    def __str__(self):
        return f"{self.nome_candidato} - {self.vaga.nome_cargo}"


# Contatos do candidato
class CandidatoEmail(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField()

    def __str__(self):
        return self.email
    

class CandidatoTelefone(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='telefones')
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.telefone
    

# Requisitos do candidato retornados do scraping (N:N)

class CandidatoFonteBusca(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='fontes_busca')
    fonte = models.ForeignKey(FonteBusca, on_delete=models.CASCADE)
    data_coleta = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidato', 'fonte')

    def __str__(self):
        return f"{self.candidato.nome_candidato} - {self.fonte}"
    

class CandidatoHabilidadeTecnica(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='habilidades_tecnicas')
    habilidade = models.ForeignKey(HabilidadeTecnica, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidato.nome_candidato} - {self.habilidade.nome}"
    

class CandidatoHabilidadeInterpessoal(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='habilidades_interpessoais')
    habilidade = models.ForeignKey(HabilidadeInterpessoal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidato.nome_candidato} - {self.habilidade.nome}"
    

class CandidatoDiploma(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='diplomas')
    diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidato.nome_candidato} - {self.diploma}"
    

class CandidatoCertificacao(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='certificacoes')
    certificacao = models.ForeignKey(Certificacao, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidato.nome_candidato} - {self.certificacao.nome}"
    

class CandidatoIdioma(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='idiomas')
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidato.nome_candidato} - {self.idioma.nome}"


class CandidatoEmpresa(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='empresas')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidato.nome_candidato} - {self.empresa.nome}"
    

class CandidatoLocalizacao(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='localizacoes')
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidato.nome_candidato} - {self.localizacao}"
