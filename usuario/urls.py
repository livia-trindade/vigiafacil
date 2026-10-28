from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('login/', views.login_usuario, name='login-usuario'),
    path('logout/', views.logout_usuario, name='logout-usuario'),

    # Gerenciamento de usuários
    path('criar/', views.criar_usuario, name='criar-usuario'),
    path('', views.listar_usuarios, name='listar-usuarios'),
    path(
        '<int:id_usuario>/',
        views.detalhar_usuario,
        name='detalhar-usuario'
    ),
    path(
        '<int:id_usuario>/editar/',
        views.editar_usuario,
        name='editar-usuario'
    ),
    path(
        '<int:id_usuario>/excluir/',
        views.excluir_usuario,
        name='excluir-usuario'
    ),
]
