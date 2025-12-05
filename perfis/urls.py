from django.urls import path

from perfis import views

app_name = "perfis"

urlpatterns = [
    path("perfil/<slug>", views.PerfilDetailView.as_view(), name="perfil"),
    path("perfil/<pk>/delete", views.PerfilDeleteView.as_view(), name="delete"),
    path('registra', views.PerfilRegisterView.as_view(), name="registra"),
    path('<int:user_id>/atualiza', views.PerfilUpdateView.as_view(), name="atualiza"),
    path('peso/registra', views.PerfilPesoImcCreateView.as_view(), name="peso_registro"),
    path('peso/lista', views.PerfilPersoImcListView.as_view(), name="peso_lista"),
    path('peso/<pk>/update', views.PerfilPesoImcUpdateView.as_view(), name="peso_atualiza"),
    path('peso/<pk>/delete', views.PerfilPesoImcDeleteView.as_view(), name="peso_delete"),
    path("biotipo", views.PerfilBiotipoListView.as_view(), name="biotipo_lista"),
    path("biotipo/<pk>/atualiza", views.PerfilBiotipoUpdateView.as_view(), name="biotipo_atualiza"),
    path("biotipo/registra", views.PerfilBiotipoCreateView.as_view(), name="biotipo_registro"),
    path("biotipo/<pk>/delete", views.PerfilBiotipoDeleteView.as_view(), name="biotipo_delete"),

]
