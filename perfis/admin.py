from django.contrib import admin

from perfis.models import Perfil, HistoricoPesoImc


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'telefone', 'sexo','slug')
    fields = ('user',
              'nome_completo',
              'telefone',
              'data_nascimento',
              'sexo',
              'altura',
              'tipo_sanguineo',
              'tipo_diabetes',
              'tempo_diagnostico',
              'insulina',
              'medicamentos_utilizados',
              'alergias',
              'outras_condicoes',
              'slug')

@admin.register(HistoricoPesoImc)
class PerfilHistoricoPesoImc(admin.ModelAdmin):
    list_display = ('perfil', 'peso', 'imc')
    fields = ('perfil','peso')