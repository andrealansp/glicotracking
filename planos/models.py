from django.db import models
from tinymce import models as tinymce_models

from core.models import Tag


class Plano(models.Model):
    TIPO_REFEICAO_CHOICES = [
        ('cafe_manha', 'Café da Manhã'),
        ('almoco', 'Almoço'),
        ('jantar', 'Jantar'),
        ('lanche_manha', 'Lanche da Manhã'),
        ('lanche_tarde', 'Lanche da Tarde'),
        ('ceia', 'Ceia'),
        # Adicione mais opções conforme necessário
    ]
    tipo_refeicao = models.CharField(max_length=20, choices=TIPO_REFEICAO_CHOICES, verbose_name='Tipo de Refeição')
    titulo = models.CharField(verbose_name='titulo', max_length=100,blank=True, null=True)
    cardapio = tinymce_models.HTMLField(verbose_name='Cardápio',blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name='Tag', related_name='tag', blank=True)

    def __str__(self):
        return f"{self.get_tipo_refeicao_display()}: {self.titulo}"

    class Meta:
        app_label = 'planos'
        verbose_name_plural = 'Planos'
        unique_together = ('tipo_refeicao', 'cardapio')
