import secrets
import string

from django.db import models

class Denuncia(models.Model):

    TIPO_DENUNCIA = [
        ('agua', 'Água e saneamento'),
        ('alimentos', 'Alimentos'),
        ('vetores', 'Vetores e pragas'),
        ('animais', 'Animais'),
        ('estabelecimento', 'Estabelecimento de saúde'),
        ('outros', 'Outros'),
    ]

    STATUS_DENUNCIA = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em análise'),
        ('em_andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
    ]

    protocolo = models.CharField(
        max_length=20,
        unique=True
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_DENUNCIA
    )

    descricao = models.TextField()
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100)

    data_ocorrencia = models.DateField(
        blank=True,
        null=True
    )

    # Controle interno
    status = models.CharField(
        max_length=20,
        choices=STATUS_DENUNCIA,
        default='pendente'
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True
    )

    protocolo = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'denuncia_denuncia'
        ordering = ['-data_criacao']
        verbose_name = 'Denúncia'
        verbose_name_plural = 'Denúncias'


    def save(self, *args, **kwargs):
        if not self.protocolo:
            caracteres = string.ascii_letters + string.digits

            while True:
                protocolo = ''.join(
                    secrets.choice(caracteres) for _ in range(10)
                )

                if not Denuncia.objects.filter(
                    protocolo=protocolo
                ).exists():
                    self.protocolo = protocolo
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Denúncia {self.protocolo}'