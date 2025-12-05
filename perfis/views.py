from urllib.parse import uses_query

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from perfis.forms import RegistroForm, PerfilUpdateForm, HistoricoPesoImcForm, HistoricoBiotipoForm
from perfis.models import Perfil, HistoricoPesoImc, HistoricoBioTipo


class CustomLoginView(LoginView):
    def get_success_url(self):
        perfil = self.request.user.perfil
        if not perfil.perfil_completo():
            return reverse('perfis:atualiza', kwargs={"user_id":perfil.user.id})
        return super().get_success_url()


class PerfilRegisterView(CreateView):
    template_name = "perfis/perfil_register_user.html"
    form_class = RegistroForm

    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        Perfil.objects.create(
            user=user,
            nome_completo=form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name'],
            telefone=form.cleaned_data['telefone'],
            data_nascimento=form.cleaned_data['data_nascimento'],
            sexo=form.cleaned_data['sexo'],
        )
        messages.success(self.request,"Usuário cadastrado com sucesso!")
        return HttpResponseRedirect(reverse('login'))

    def form_invalid(self, form):
        return super().form_invalid(form)


class PerfilDetailView(LoginRequiredMixin, DetailView):
    model = Perfil
    template_name_suffix = '_detail'
    context_object_name = "perfil"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('slug')

        try:
            if slug != self.request.user.perfil.slug:
                raise Http404("Perfil não encontrado")
            perfil = queryset.get(slug=slug)
            return perfil
        except queryset.model.DoesNotExist:
            raise Http404("Perfil não encontrado")


class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = Perfil
    form_class = PerfilUpdateForm
    template_name_suffix = '_form'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        user_id = self.kwargs.get('user_id')

        try:
            perfil = queryset.get(user__id=user_id)
            return perfil
        except queryset.model.DoesNotExist:
            raise Http404("Perfil não encontrado")

    def form_valid(self, form):
        form.save()
        slug = form.cleaned_data['slug']
        return HttpResponseRedirect(reverse_lazy('perfis:perfil', kwargs={'slug': slug}))

class PerfilDeleteView(LoginRequiredMixin, DeleteView):
    model = Perfil
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy("login")


class PerfilPesoImcCreateView(LoginRequiredMixin, CreateView):
    model = HistoricoPesoImc
    form_class = HistoricoPesoImcForm
    template_name_suffix = '_form'
    success_url = reverse_lazy('perfis:peso_lista')

    def form_valid(self, form):
        perfil = Perfil.objects.get(user=self.request.user)
        form.instance.perfil = perfil
        return super().form_valid(form)


class PerfilPersoImcListView(LoginRequiredMixin, ListView):
    model = HistoricoPesoImc
    template_name_suffix = '_listar'
    context_object_name = "peso"

    def get_queryset(self):
        instancia = super().get_queryset().filter(perfil=self.request.user.perfil)
        return instancia


class PerfilPesoImcUpdateView(LoginRequiredMixin, UpdateView):
    model = HistoricoPesoImc
    form_class = HistoricoPesoImcForm
    template_name_suffix = '_form'
    success_url = reverse_lazy('perfis:peso_lista')

    def form_valid(self, form):
        perfil = Perfil.objects.get(user=self.request.user)
        form.instance.perfil = perfil
        return super().form_valid(form)


class PerfilPesoImcDeleteView(LoginRequiredMixin, DeleteView):
    model = HistoricoPesoImc
    queryset = HistoricoPesoImc.objects.all()
    success_url = reverse_lazy("perfis:peso_lista")


class PerfilBiotipoListView(LoginRequiredMixin, ListView):
    model = HistoricoBioTipo
    template_name_suffix = '_listar'
    context_object_name = "biotipo"

    def get_queryset(self):
        instancia = super().get_queryset().filter(perfil=self.request.user.perfil)
        return instancia


class PerfilBiotipoUpdateView(LoginRequiredMixin, UpdateView):
    model = HistoricoBioTipo
    fields = "__all__"
    success_url = reverse_lazy("perfis:biotipo_lista")


class PerfilBiotipoCreateView(LoginRequiredMixin, CreateView):
    model = HistoricoBioTipo
    form_class = HistoricoBiotipoForm
    success_url = reverse_lazy("perfis:biotipo_lista")

    def form_valid(self, form):
        perfil = Perfil.objects.get(user=self.request.user)
        form.instance.perfil = perfil
        return super().form_valid(form)


class PerfilBiotipoDeleteView(LoginRequiredMixin, DeleteView):
    model = HistoricoBioTipo
    queryset = HistoricoBioTipo.objects.all()
    success_url = reverse_lazy("perfis:biotipo_lista")
