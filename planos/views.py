from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Plano

class PlanoListView(LoginRequiredMixin, ListView):
    template_name = "planos/plano_list.html"
    model = Plano

class PlanoCreateView(LoginRequiredMixin, CreateView):
    model = Plano
    fields = "__all__"
    success_url = reverse_lazy("planos:lista")

class PlanoUpdateView(LoginRequiredMixin, UpdateView):
    model = Plano
    fields = "__all__"
    success_url = reverse_lazy("planos:lista")

class PlanoDeleteView(LoginRequiredMixin, DeleteView):
    model = Plano
    queryset = Plano.objects.all()
    success_url = reverse_lazy("planos:lista")


class PlanoDetailView(LoginRequiredMixin, DetailView):
    model = Plano
    queryset = Plano.objects.all()
