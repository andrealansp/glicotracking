from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

import medicoes
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
        data_medicao_data = self.request.GET.get('mes')

        if tipo_medicao_data:
            instancia = instancia.filter(tipo_medicao=tipo_medicao_data)
        if data_medicao_data:
            instancia = instancia.filter(data_medicao=data_medicao_data)


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
