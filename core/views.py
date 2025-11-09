from datetime import datetime

from django.views.generic import TemplateView
from django.db.models import Avg
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

        perfil = self.request.user.perfil  # Assumindo que cada usuário tem um perfil relacionado

        # --- Dados para o gráfico de glicose ---
        glicose_diaria = (Medicao.objects.filter(perfil=perfil,data_medicao__month=datetime.today().month).
                          annotate(data=TruncDate('data_medicao')).values('data').
                          annotate(media=Avg('valor_glicose')).order_by('data'))

        

        glicose_diaria_lista = [{'data': item['data'].isoformat(), 'media': item['media']} for item in glicose_diaria]

        glicose_mensal = (Medicao.objects.filter(perfil=perfil).
                          annotate(mes=TruncMonth('data_medicao')).values('mes').
                          annotate(media=Avg('valor_glicose')).order_by('mes'))

        glicose_mensal_lista = [
            {'mes': item['mes'].isoformat(),
             'media': item['media']} for item in
            glicose_mensal]

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

        context['glicose_diaria'] = json.dumps(glicose_diaria_lista, cls=DjangoJSONEncoder)
        context['glicose_mensal'] = json.dumps(glicose_mensal_lista, cls=DjangoJSONEncoder)
        context['historico_peso_imc'] = json.dumps(historico_peso_imc_lista, cls=DjangoJSONEncoder)
        context['historico_biotipo'] = json.dumps(historico_biotipo_lista, cls=DjangoJSONEncoder)

        return context
