from django.urls import path
from django.contrib.auth import views as auth_views

import perfis.views

app_name = "contas"
urlpatterns = [
    path("login/",
         perfis.views.CustomLoginView.as_view(),
         name='login'
         ),
    path("logout",
         auth_views.LogoutView.as_view(),
         name="logout"
         ),
    path("troca_de_senha",
         auth_views.PasswordChangeView.as_view(success_url="/contas/senha_atualizada"),
         name="troca_senha"
         ),
    path("senha_atualizada",
         auth_views.PasswordChangeDoneView.as_view(),
         name="sucesso"
         ),
    path("reset_senha",
         auth_views.PasswordResetView.as_view(success_url="reset_senha_enviado"),
         name="reset_senha"
         ),
    path("reset_senha_enviado",
         auth_views.PasswordResetDoneView.as_view(),
         name="reset_senha_enviado"
         ),
    path("reset_senha_confirmado/<uidb64>/<token>",
         auth_views.PasswordResetConfirmView.as_view(success_url="/contas/reset_senha_finalizado"),
         name="reset_senha_confirmado"
         ),
    path("reset_senha_finalizado",
         auth_views.PasswordResetCompleteView.as_view(),
         name="reset_senha_finalizado"
         )
]