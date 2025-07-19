from django.db import models

from perfis.models import Perfil


class Exame(models.Model):
    data_exame = models.DateField(verbose_name='Data do Exame')
    medico = models.CharField(max_length=100, verbose_name='Médico')
    especialidade = models.CharField(max_length=100, verbose_name='Especialidade do Médico', null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True, verbose_name='Observações')
    exame_arquivo = models.FileField(upload_to='exames', verbose_name='Arquivo',null=True, blank=True)
    perfil = models.ForeignKey(Perfil, verbose_name='Perfil', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.medico} - {self.data_exame.strftime('%d/%m/%Y')}"

    class Meta:
        app_label = 'exames'
        verbose_name = 'Exame'
        verbose_name_plural = 'Exames'
        ordering = ['-data_exame']