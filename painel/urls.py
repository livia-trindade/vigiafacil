from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard-painel'),
    path(
        'denuncia/<int:id_denuncia>/',
        views.detalha,
        name='detalha-painel'
    ),
    path(
        'denuncia/<int:id_denuncia>/status/',
        views.atualizar_status,
        name='atualizar-status'
    ),
    path(
        'denuncia/<int:id_denuncia>/acompanhamento/',
        views.registrar_acompanhamento,
        name='registrar-acompanhamento'
    ),
]