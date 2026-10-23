
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.index, name='index-denuncia'),
    path('<int:id_denuncia>/', views.detalha, name='detalha-denuncia'),
    path('create/', views.create, name='create-denuncia'),
    path('update/<int:id_denuncia>/', views.update, name='update-denuncia'),
    path('delete/<int:id_denuncia>/', views.delete, name='delete-denuncia'),
    path('sucesso/', views.sucesso, name='sucesso-denuncia'),
]
