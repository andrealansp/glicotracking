import datetime
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


def add_tempo():
    return datetime.date.today() + timedelta(days=30)


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    nome_completo = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    altura = models.FloatField("Altura", help_text="Altura em CM", blank=True, null=True)
    tipo_sanguineo = models.CharField("Tipo Sanguíneo", max_length=3, blank=True, null=True)
    tipo_diabetes = models.CharField("Tipo Diabetes", max_length=10, choices=[('tipo1', 'Tipo 1'), ('tipo2', "Tipo 2")],
                                     blank=True, null=True)
    tempo_diagnostico = models.IntegerField("Tempo de Diagnóstico", help_text="Ano da Descoberta", blank=True, null=True)
    insulina = models.CharField("Usa Insulina?", help_text="Insulina", choices=[('sim', 'Sim'), ('não', 'Não')],
                                blank=True, null=True)
    medicamentos_utilizados = models.TextField("Medicamentos Utilizados", blank=True, null=True)
    alergias = models.TextField("Alergias", blank=True, null=True)
    outras_condicoes = models.TextField(blank=True)
    primeiro_login_completo = models.BooleanField(default=False)
    peso_desejado = models.FloatField("Peso Desejado", help_text="Peso desejado para alcançar", blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)


    def perfil_completo(self):
        return all([
            self.nome_completo,
            self.data_nascimento,
            self.telefone,
            self.peso_desejado,
            self.sexo,
            self.altura,
            self.tipo_sanguineo,
            self.tipo_diabetes,
            self.tempo_diagnostico,
            self.insulina,
        ])

    def save(self, *args, **kwargs):
        slug = slugify(self.nome_completo)
        self.slug = slug
        super(Perfil, self).save(*args, **kwargs)


    class Meta:
        app_label = 'perfis'
        ordering = ["-data_nascimento"]
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return f'{self.nome_completo}'

class HistoricoPesoImc(models.Model):
    perfil = models.ForeignKey(Perfil,related_name='perfilpeso', on_delete=models.CASCADE)
    data_registro = models.DateField(auto_now_add=True)
    peso = models.DecimalField("Peso",help_text="Peso em Kg",max_digits=5, decimal_places=2, null=False, blank=False)
    imc = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    grau_obesidade = models.CharField("Grau de Obesidade", max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        altura_m = self.perfil.altura / 100
        self.imc = round(float(self.peso) / (altura_m ** 2), 2)
        self.grau_obesidade = self.get_grau_obesidade(self.imc)
        super().save(*args, **kwargs)

    @staticmethod
    def get_grau_obesidade(imc):
        if imc < 18.5:
            return 'Abaixo do peso'
        elif 18.5 <= imc < 24.9:
            return 'Peso normal'
        elif 25.9 <= imc < 29.9:
            return 'Sobrepeso'
        elif 30 <= imc < 34.9:
            return 'Obesidade grau I'
        elif 35 <= imc < 39.9:
            return 'Obesidade grau II'
        elif imc >= 40.0:
            return 'Obesidade grau III'
        return None

    class Meta:
        ordering = ["-peso"]
        verbose_name = "Historico Peso Imc"
        verbose_name_plural = "Historicos Peso Imc"

    def __str__(self):
        return f"{self.peso} - {self.data_registro}"

class HistoricoBioTipo(models.Model):
    perfil = models.ForeignKey(Perfil,related_name='perfilbiotipo', on_delete=models.CASCADE)
    data_registro = models.DateField(default=datetime.date.today, editable=False)
    proximo_registro = models.DateField(editable=False, default=add_tempo)
    cintura = models.FloatField("Cintura", help_text="Cintura em CM", blank=False, null=False)
    quadril = models.FloatField("Quadril", help_text="Quadril em CM", blank=False, null=False)
    braco = models.FloatField("Braço", help_text="Circunferência do braco em CM", blank=True, null=True)
    perna = models.FloatField("Pernas", help_text="Circunferência da perna em CM", blank=True, null=True)
    abdomen = models.FloatField("Abdômen", help_text="Circunferência abdominal em CM", blank=True, null=True)

    class Meta:
        ordering = ["-data_registro"]
        verbose_name = "Historico Peso Imc"
        verbose_name_plural = "Historicos Peso Imc"

    def __str__(self):
        return f"Cintura: {self.cintura} - Quadril: {self.quadril}"

