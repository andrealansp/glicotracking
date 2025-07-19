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
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
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
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)


    def perfil_completo(self):
        return all([
            self.nome_completo,
            self.data_nascimento,
            self.telefone,
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
    peso_kg = models.DecimalField("Peso",help_text="Peso em Kg",max_digits=5, decimal_places=2, null=False, blank=False)
    imc = models.DecimalField(max_digits=5, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        altura_m = self.perfil.altura / 100
        self.imc = round(float(self.peso_kg) / (altura_m ** 2), 2)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-peso_kg"]
        verbose_name = "Historico Peso Imc"
        verbose_name_plural = "Historicos Peso Imc"

    def __str__(self):
        return f"{self.peso_kg} - {self.data_registro}"

class HistoricoBioTipo(models.Model):
    perfil = models.ForeignKey(Perfil,related_name='perfilbiotipo', on_delete=models.CASCADE)
    data_registro = models.DateField(default=datetime.date.today, editable=False)
    proximo_registro = models.DateField(editable=False, default=add_tempo)
    cintura = models.FloatField("Cintura", help_text="Cintura em CM", blank=False, null=False)
    quadril = models.FloatField("Quadril", help_text="Quadril em CM", blank=False, null=False)

    class Meta:
        ordering = ["-data_registro"]
        verbose_name = "Historico Peso Imc"
        verbose_name_plural = "Historicos Peso Imc"

    def __str__(self):
        return f"Cintura: {self.cintura} - Quadril: {self.quadril}"

