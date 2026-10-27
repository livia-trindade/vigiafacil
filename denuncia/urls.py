from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index-denuncia'),
    path('registro/', views.registro, name='registro-denuncia'),
    path(
        'sucesso/<str:protocolo>/',
        views.sucesso,
        name='sucesso-denuncia'
    ),
    path(
        '<int:id_denuncia>/',
        views.detalha,
        name='detalha-denuncia'
    ),
    path(
        'update/<int:id_denuncia>/',
        views.update,
        name='update-denuncia'
    ),
    path(
        'delete/<int:id_denuncia>/',
        views.delete,
        name='delete-denuncia'
    ),
]