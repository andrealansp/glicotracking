from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from exames.forms import ExameForm
from exames.models import Exame
from perfis.models import Perfil


# Create your views here.

class ExameListView(LoginRequiredMixin, ListView):
    model = Exame
    template_name = 'perfil_list.html'

    def get_queryset(self):
        instancia = super().get_queryset().filter(perfil=self.request.user.perfil)
        return instancia


class CreateExameView(LoginRequiredMixin, View):
    model = Exame
    template_name = 'exames/exame_form.html'
    form_class = ExameForm
    success_url = reverse_lazy('exames:lista')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            perfil = Perfil.objects.get(user=self.request.user)
            form.instance.perfil = perfil
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})

class UpdateExameView(LoginRequiredMixin, UpdateView):
    model = Exame
    form_class = ExameForm
    template_name = 'exames/exame_form.html'
    success_url = "/exames/lista/"

class DeleteExameView(LoginRequiredMixin, DeleteView):
    model = Exame
    template_name = 'exames/exame_confirm_delete.html'
    query_set = Exame.objects.all()
    success_url = '/exames/lista/'
