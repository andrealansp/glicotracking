import json

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from medicoes.forms import MedicaoForm,MedicaoFilterForm
from medicoes.models import Medicao
from perfis.models import Perfil

# Create your views here.

class MedicoesListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_listar"
    model = Medicao

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MedicaoFilterForm(self.request.GET or None)
        return context

    def get_queryset(self):
        instancia = super().get_queryset().all()
        tipo_medicao_data = self.request.GET.get('tipo_medicao')
        mes = self.request.GET.get('mes')

        if tipo_medicao_data:
            instancia = instancia.filter(tipo_medicao=tipo_medicao_data)
        if mes:
            instancia = instancia.filter(data_medicao__month=mes)


        return instancia


class MedicoesCreateView(LoginRequiredMixin, CreateView):
    model = Medicao
    form_class = MedicaoForm
    success_url = reverse_lazy("medicoes:lista")

    def form_valid(self, form):
        perfil = Perfil.objects.get(user=self.request.user)
        form.instance.perfil = perfil
        return super().form_valid(form)


class MedicoesUpdateView(LoginRequiredMixin, UpdateView):
    model = Medicao
    form_class = MedicaoForm
    success_url = reverse_lazy("medicoes:lista")

    def form_valid(self, form):
        perfil = Perfil.objects.get(user=self.request.user)
        form.instance.perfil = perfil
        return super().form_valid(form)


class MedicoesDeleteView(LoginRequiredMixin, DeleteView):
    model = Medicao
    queryset = Medicao.objects.all()
    success_url = reverse_lazy("medicoes:lista")


class RelatoriosListView(LoginRequiredMixin, ListView):
    template = "medicao_relatorio.html"
    template_name_suffix = "_relatorio"
    model = Medicao

    def get_queryset(self):
        instancia = super().get_queryset().all()
        tipo_medicao_data = self.request.GET.get('tipo_medicao')
        mes = self.request.GET.get('mes')

        if tipo_medicao_data:
            instancia = instancia.filter(tipo_medicao=tipo_medicao_data)
        if mes:
            instancia = instancia.filter(data_medicao__month=mes)

        return instancia

    def get_context_data(self, **kwargs):

        dados_lista = []
        for medicao in self.object_list:
            dados_lista.append({
                'data': medicao.data_medicao.isoformat(),
                'valor': float(medicao.valor_glicose),
            })

        context = super().get_context_data(**kwargs)
        context["dados_json"] = json.dumps(dados_lista)

        return context

