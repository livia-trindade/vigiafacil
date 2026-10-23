from django.db import models
from denuncia.models import Denuncia
from django.contrib.auth.models import User


class Acompanhamento(models.Model):

    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='acompanhamentos'
    )

    vigilante = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    descricao = models.TextField(
        verbose_name='Descrição da providência'
    )

    data_registro = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'painel_acompanhamento'
        ordering = ['-data_registro']
        verbose_name = 'Acompanhamento'
        verbose_name_plural = 'Acompanhamentos'

    def __str__(self):
        return f'Acompanhamento da denúncia {self.denuncia_id}'