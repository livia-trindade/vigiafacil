from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('denuncia/', include('denuncia.urls')),
    path('painel/', include('painel.urls')),
    path('usuario/', include('usuario.urls')),
]