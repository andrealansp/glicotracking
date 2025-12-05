from django.urls import path
from medicoes import views

app_name = "medicoes"

urlpatterns = [
    path("lista", views.MedicoesListView.as_view(), name="lista"),
    path("registra", views.MedicoesCreateView.as_view(), name="registra"),
    path("<int:pk>/atualiza/", views.MedicoesUpdateView.as_view(), name="atualiza"),
    path("<int:pk>/deleta/", views.MedicoesDeleteView.as_view(), name="deleta"),
    path("relatorio/",views.RelatoriosListView.as_view(), name="relatorio"),
    path("api/v1/medicoes", views.MedicoesCreateListView.as_view(), name="api-lista"),
    path("api/v1/medicoes/<int:pk>", views.MedicoesRetrieveUpdateDestroyView.as_view(), name="api-details"),
]
