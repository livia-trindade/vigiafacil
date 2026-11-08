from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index-denuncia'),
    path('setor/', views.selecionar_setor, name='setor-denuncia'),
    path('registro/', views.registro, name='registro-denuncia'),
    path(
        'sucesso/<str:protocolo>/',
        views.sucesso,
        name='sucesso-denuncia'
    ),
    path(
        'acompanhar/', 
        views.acompanhar, 
        name='acompanhar-denuncia'),
]