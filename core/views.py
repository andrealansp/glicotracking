from datetime import timedelta
from django.utils import timezone

from django.views.generic import TemplateView
from django.db.models import Avg, Min, Max
from django.db.models.functions import TruncDay, TruncMonth, TruncYear, TruncDate
from medicoes.models import Medicao
from perfis.models import HistoricoPesoImc, Perfil, HistoricoBioTipo

from django.core.serializers.json import DjangoJSONEncoder
import json

import logging

logger = logging.getLogger(__name__)

# Create your views here.
class RelatorioMedicoesView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = timezone.now()
        inicio_mes = hoje - timedelta(days=30)
        data_corte_glicada = hoje - timedelta(days=90)

        perfil = self.request.user.perfil  # Assumindo que cada usuário tem um perfil relacionado

        # --- Dados para o gráfico de peso e IMC ---
        historico_peso_imc = HistoricoPesoImc.objects.filter(perfil=perfil).order_by('data_registro')
        historico_peso_imc_lista = [
            {'data_registro': item.data_registro.isoformat(),
             'peso_kg': str(item.peso_kg),
             'imc': str(item.imc)} for
            item in historico_peso_imc]

        historico_biotipo = HistoricoBioTipo.objects.filter(perfil=perfil).order_by('data_registro')
        historico_biotipo_lista = [{
            "data_registro": item.data_registro.isoformat(),
            "cintura": item.cintura,
            "quadril": item.quadril,
            "braço": item.braco,
            "abdomen": item.abdomen,
            "perna": item.perna,
        } for item in historico_biotipo]


        medicoes = Medicao.objects.filter(perfil=perfil, data_medicao__gte=inicio_mes)
        medicoes_glicada = Medicao.objects.filter(perfil=perfil, data_medicao__gte=data_corte_glicada)

        # 1. Time in Range (TIR)
        total_medicoes = medicoes.count()
        no_alvo = medicoes.filter(valor_glicose__gte=70, valor_glicose__lte=180).count()
        tir_percent = (no_alvo / total_medicoes * 100) if total_medicoes > 0 else 0

        # 2. Glicada Estimada (Fórmula ADAG)
        media_glicose = medicoes_glicada.aggregate(Avg('valor_glicose'))['valor_glicose__avg'] or 0
        glicada_estimada = (media_glicose + 46.7) / 28.7

        # 3. Dados para o Gráfico Principal (Min/Max/Media por dia)
        # Usar TruncDay para agrupar por dia

        labels = [d.data_medicao.strftime('%d/%m') for d in medicoes]
        valor_glicose = [d.valor_glicose for d in medicoes]
        tipo_medicao = [d.tipo_medicao for d in medicoes]


        context['historico_peso_imc'] = json.dumps(historico_peso_imc_lista, cls=DjangoJSONEncoder)
        context['historico_biotipo'] = json.dumps(historico_biotipo_lista, cls=DjangoJSONEncoder)
        context["tir_percent"] = json.dumps(tir_percent, cls=DjangoJSONEncoder)
        context['glicada_estimada'] = json.dumps(glicada_estimada, cls=DjangoJSONEncoder)
        context['peso_ideal'] = perfil.peso_desejado
        context['dados_grafico'] = {
            'legendas': json.dumps(labels),
            'dados': json.dumps(valor_glicose),
            'tipo': json.dumps(tipo_medicao),
        }
        context['ultima_medicao'] = medicoes.first()


        return context
