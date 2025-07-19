from django.utils import timezone

from django.db import models
from exames.models import Exame
from perfis.models import Perfil

class Medicao(models.Model):
    TAMANHO_CHOICES = [
        ("","Tamanho das Refeições"),
        ('pequena', 'Pequena (até 299g)'),
        ('media', 'Média (300g até 499g)'),
        ('grande', 'Grande (500 até 800g)'),
    ]
    TIPO_REFEICAO_CHOICES = [
        ("","Tipo de Refeição"),
        ('cafe_manha', 'Café da Manhã'),
        ('almoco', 'Almoço'),
        ('jantar', 'Jantar'),
        ('lanche_manha', 'Lanche da Manhã'),
        ('lanche_tarde', 'Lanche da Tarde'),
        ('ceia', 'Ceia'),
    ]
    TIPO_MEDICAO_CHOICES = [
        ("","Tipo de Medição"),
        ('pre_prandial', 'Pré-Prandial'),
        ('pos_prandial_1h', 'Pós-Prandial 1 Hora'),
        ('pos_pandrial_2h', 'Pós-Pandrial 2 Horas'),
        ('jejum', 'Jejum'),
        ('aleatoria', 'Aleatória'),
    ]
    valor_glicose = models.FloatField(verbose_name='Valor da Glicose (mg/dL)')
    tipo_medicao = models.CharField(max_length=20, choices=TIPO_MEDICAO_CHOICES, verbose_name='Tipo de Medição')
    data_medicao = models.DateTimeField(verbose_name='Data da Medição', default=timezone.now)
    observacoes = models.TextField(null=True, blank=True, verbose_name='Observações')
    alimento = models.CharField(max_length=150, verbose_name='Alimento',null=True, blank=True)
    tipo_refeicao = models.CharField(max_length=20, choices=TIPO_REFEICAO_CHOICES, verbose_name='Tipo de Refeição', null=True, blank=True)
    tamanho = models.CharField(max_length=20, verbose_name='Tamanho', choices=TAMANHO_CHOICES, null=True, blank=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, verbose_name='Perfil')
    exame = models.ForeignKey(Exame, on_delete=models.SET_NULL, null=True, blank=True, related_name='medicoes', verbose_name='Exame Relacionado')


    def __str__(self):
        return f"{self.valor_glicose} mg/dL em {self.data_medicao.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        app_label = 'medicoes'
        verbose_name_plural = 'Medições'



