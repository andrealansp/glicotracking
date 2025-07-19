from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from perfis.views import CustomLoginView
urlpatterns = [
    path(
        "", RedirectView.as_view(url="/login", permanent=False), name="index"
    ),
    path('tinymce/', include('tinymce.urls')),
    path("admin/", admin.site.urls),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("core/", include("core.urls")),
    path("medicoes/", include("medicoes.urls")),
    path("planos/", include("planos.urls")),
    path("exames/", include("exames.urls")),
    path("perfis/", include("perfis.urls")),
]

if settings.DEBUG:
    # Servindo statics em desenvolvimento
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Servindo media em desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
