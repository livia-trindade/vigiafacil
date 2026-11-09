import secrets
import string

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import models


# Perguntas de cada setor (etapa 1 do registro).
# Cada texto é mostrado na tela com um "?" no final.
PROBLEMAS_POR_CATEGORIA = {
    'zoonose': [
        ('animais_peconhentos', 'Animais peçonhentos'),
        ('suspeita_raiva', 'Animais com suspeita de raiva'),
        ('colonia_animais', 'Colônia de animais'),
    ],
    'endemias': [
        ('foco_dengue', 'Foco de dengue'),
        ('insetos_geral', 'Insetos no geral'),
    ],
    'vigilancia_sanitaria': [
        ('alimentos_improprios', 'Alimentos estragados ou contaminados'),
        ('estabelecimentos_insalubres', 'Estabelecimentos insalubres'),
        ('falta_higiene_servico', 'Falta de higiene na prestação de um serviço'),
    ],
    'saude_trabalhador': [
        ('falta_epi', 'Falta de EPI'),
        ('condicoes_insalubres', 'Condições de trabalho insalubres'),
        ('risco_ambiente_trabalho', 'Risco no ambiente de trabalho'),
    ],
    'saude_ambiental': [
        ('agua_contaminada', 'Água contaminada'),
        ('esgotos', 'Esgotos'),
        ('descarte_residuos', 'Descarte de resíduos'),
        ('solo_contaminado', 'Solo contaminado'),
        ('poluicao_ar_fumaca', 'Poluição no ar ou fumaça'),
    ],
    'outros': [
        ('outro_problema', 'Outra opção não apresentada aqui'),
    ],
}

TODOS_OS_PROBLEMAS = [
    problema
    for problemas in PROBLEMAS_POR_CATEGORIA.values()
    for problema in problemas
]


class Denuncia(models.Model):

    TIPO_DENUNCIA = [
        ('zoonose', 'Zoonose'),
        ('endemias', 'Endemias'),
        ('vigilancia_sanitaria', 'Vigilância Sanitária'),
        ('saude_trabalhador', 'Vigilância em Saúde do Trabalhador'),
        ('saude_ambiental', 'Vigilância em Saúde Ambiental'),
        ('outros', 'Outros'),
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

    # Setor principal (o primeiro marcado "Sim" na etapa 1).
    # A lista completa de setores fica em ClassificacaoDenuncia.
    tipo = models.CharField(
        max_length=30,
        choices=TIPO_DENUNCIA,
        verbose_name='Categoria'
    )

    # Não é mais preenchido pela etapa 1 (a resposta vale para o setor inteiro).
    problema = models.CharField(
        max_length=40,
        choices=TODOS_OS_PROBLEMAS,
        blank=True,
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

    # Senha de acompanhamento (guardada apenas como hash)
    senha_hash = models.CharField(
        max_length=128,
        blank=True,
        verbose_name='Senha de acompanhamento'
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

        # Se houver problema, ele precisa pertencer ao setor selecionado
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

    def definir_senha(self, senha_pura):
        self.senha_hash = make_password(senha_pura)

    def conferir_senha(self, senha_pura):
        return bool(self.senha_hash) and check_password(senha_pura, self.senha_hash)

    def lista_setores(self):
        """Nomes de todos os setores da denúncia (sem repetir)."""
        nomes = dict(self.TIPO_DENUNCIA)
        setores = [
            nomes.get(item.tipo, item.tipo)
            for item in self.classificacoes.all()
        ]
        return setores or [self.get_tipo_display()]

    def __str__(self):
        return f'Denúncia {self.protocolo}'


class ClassificacaoDenuncia(models.Model):
    """Um registro para cada setor marcado "Sim" na etapa 1."""

    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='classificacoes'
    )

    tipo = models.CharField(
        max_length=30,
        choices=Denuncia.TIPO_DENUNCIA
    )

    class Meta:
        db_table = 'denuncia_classificacao'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['denuncia', 'tipo'],
                name='classificacao_setor_unico'
            )
        ]

    def __str__(self):
        return f'{self.denuncia.protocolo} - {self.tipo}'