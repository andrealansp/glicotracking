from django.urls import path

from planos import views

app_name = "planos"
urlpatterns = [
    path("lista", views.PlanoListView.as_view(), name="lista"),
    path("registra", views.PlanoCreateView.as_view(), name="registra"),
    path("atualiza/<int:pk>", views.PlanoUpdateView.as_view(), name="atualiza"),
    path("visualiza/<int:pk>", views.PlanoDetailView.as_view(), name="visualiza"),
    path("deleta/<int:pk>", views.PlanoDeleteView.as_view(), name="deleta"),
]
