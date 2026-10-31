
from django import forms
from .models import Denuncia, TODOS_OS_PROBLEMAS, PROBLEMAS_POR_CATEGORIA


class DenunciaForm(forms.ModelForm):

    class Meta:
        model = Denuncia

        fields = [
            'tipo',
            'problema',
            'descricao',
            'endereco',
            'ponto_referencia',
            'bairro',
            'data_ocorrencia',
            'foto',
            'anonima',
            'nome_denunciante',
            'telefone_denunciante',
        ]

        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_tipo',
            }),

            'problema': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_problema',
            }),

            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o problema encontrado...',
            }),

            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Informe o endereço da ocorrência',
            }),

            'ponto_referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Informe um ponto de referência',
            }),

            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Informe o bairro',
            }),

            'data_ocorrencia': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'foto': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),

            'anonima': forms.CheckboxInput(attrs={
                'id': 'id_anonima',
            }),

            'nome_denunciante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo',
            }),

            'telefone_denunciante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefone para contato',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tipo = (
            self.data.get('tipo')
            or self.initial.get('tipo')
            or getattr(self.instance, 'tipo', '')
        )

        problemas = PROBLEMAS_POR_CATEGORIA.get(tipo, [])

        self.fields['problema'].choices = [
            ('', 'Selecione um problema')
        ] + problemas

        self.fields['problema'].required = True

    def clean(self):
        cleaned_data = super().clean()

        anonima = cleaned_data.get('anonima')
        nome = cleaned_data.get('nome_denunciante')
        telefone = cleaned_data.get('telefone_denunciante')

        if not anonima:
            if not nome:
                self.add_error(
                    'nome_denunciante',
                    'Informe seu nome para realizar uma denúncia identificada.'
                )

            if not telefone:
                self.add_error(
                    'telefone_denunciante',
                    'Informe seu telefone para realizar uma denúncia identificada.'
                )

        return cleaned_data
