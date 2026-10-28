from django.db import models
from django.contrib.auth.models import User

# Criando a classe Usuario, que herda o modelo padrão de usuário do Django
class Usuario(User):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Definindo o nome da tabela no banco de dados
        db_table = "usuarios_usuarios"
        # Criando uma permissão 
        permissions = [
            ("detail_usuario", "Pode ver o detalhe de usuário"),
        ]

    # Definindo como o objeto será representado como string 
    def __str__(self):
        return self.nome