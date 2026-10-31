
import secrets
import string

from django.db import models
from django.core.exceptions import ValidationError


PROBLEMAS_POR_CATEGORIA = {
    'mosquitos_insetos': [
        ('dengue', 'Dengue'),
        ('barbeiro', 'Barbeiro'),
        ('carrapatos', 'Carrapatos'),
        ('outros_insetos', 'Outros problemas relacionados a mosquitos e insetos'),
    ],
    'animais': [
        ('animal_peconhento', 'Animal peçonhento'),
        ('animal_silvestre', 'Animal silvestre'),
        ('suspeita_raiva', 'Suspeita de raiva'),
        ('maus_tratos_abandono', 'Maus-tratos ou abandono'),
    ],
    'alimentacao_mercado': [
        ('comida_estragada', 'Comida estragada'),
        ('sujeira', 'Sujeira'),
        ('suspeita_contaminacao', 'Suspeita de contaminação'),
    ],
    'agua_esgoto': [
        ('agua_suja_cheiro', 'Água suja ou com cheiro'),
        ('esgoto_ceu_aberto', 'Esgoto a céu aberto'),
        ('poco_contaminado', 'Poço contaminado'),
    ],
    'empresas_trabalho': [
        ('falta_epi', 'Falta de EPI'),
        ('poeira_fumaca', 'Poeira ou fumaça excessiva'),
        ('condicoes_insalubres', 'Condições insalubres'),
    ],
    'outro': [
        ('outro_problema', 'Outro problema'),
    ],
}

TODOS_OS_PROBLEMAS = [
    problema
    for problemas in PROBLEMAS_POR_CATEGORIA.values()
    for problema in problemas
]


class Denuncia(models.Model):

    TIPO_DENUNCIA = [
        ('mosquitos_insetos', 'Mosquitos e insetos'),
        ('animais', 'Animais'),
        ('alimentacao_mercado', 'Alimentação e mercado'),
        ('agua_esgoto', 'Água e esgoto'),
        ('empresas_trabalho', 'Empresas e locais de trabalho'),
        ('outro', 'Outro'),
    ]

    STATUS_DENUNCIA = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em análise'),
        ('em_andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
    ]

    protocolo = models.CharField(
        max_length=10,
        unique=True,
        blank=True
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPO_DENUNCIA,
        verbose_name='Categoria'
    )

    problema = models.CharField(
        max_length=40,
        choices=TODOS_OS_PROBLEMAS,
        verbose_name='Problema específico'
    )

    descricao = models.TextField(
        verbose_name='Descrição do problema'
    )

    endereco = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Endereço'
    )

    ponto_referencia = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ponto de referência'
    )

    bairro = models.CharField(
        max_length=100
    )

    data_ocorrencia = models.DateField(
        blank=True,
        null=True
    )

    foto = models.ImageField(
        upload_to='denuncias/',
        blank=True,
        null=True,
        verbose_name='Fotografia'
    )

    anonima = models.BooleanField(
        default=True,
        verbose_name='Denúncia anônima'
    )

    nome_denunciante = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Nome do denunciante'
    )

    telefone_denunciante = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Telefone do denunciante'
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

    class Meta:
        db_table = 'denuncia_denuncia'
        ordering = ['-data_criacao']
        verbose_name = 'Denúncia'
        verbose_name_plural = 'Denúncias'

    def clean(self):
        super().clean()

        erros = {}

        # Verifica se o problema pertence à categoria selecionada
        problemas_validos = dict(
            PROBLEMAS_POR_CATEGORIA.get(self.tipo, [])
        )

        if self.problema and self.problema not in problemas_validos:
            erros['problema'] = (
                'Selecione um problema correspondente à categoria escolhida.'
            )

        # Exige endereço ou ponto de referência
        if not self.endereco and not self.ponto_referencia:
            erros['endereco'] = (
                'Informe o endereço ou um ponto de referência da ocorrência.'
            )

        if erros:
            raise ValidationError(erros)

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
