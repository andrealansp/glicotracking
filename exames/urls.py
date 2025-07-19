from django.urls import path
from exames import views
app_name = "exames"
urlpatterns = [
    path('lista/', views.ExameListView.as_view(), name='lista'),
    path('cadastra/', views.CreateExameView.as_view(), name='cadastra'),
    path('<int:pk>/atualiza', views.UpdateExameView.as_view(), name='atualiza'),
    path('<int:pk>/deleta/', views.DeleteExameView.as_view(), name='deleta'),
]
