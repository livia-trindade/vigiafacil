
from django import forms
from .models import Denuncia
from django.utils import timezone
import re


class DenunciaForm(forms.ModelForm):

    class Meta:
        model = Denuncia

        fields = [
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
                'max': timezone.localdate().isoformat(),
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
 
        # Calculado a cada abertura do formulário (e não quando o servidor inicia)
        self.fields['data_ocorrencia'].widget.attrs['max'] = (
            timezone.localdate().isoformat()
        )

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

    def clean_data_ocorrencia(self):
        data = self.cleaned_data.get('data_ocorrencia')

        if data and data > timezone.localdate():
            raise forms.ValidationError(
                'A data da ocorrência não pode ser futura.'
            )

        return data


class SenhaDenunciaForm(forms.Form):

    senha = forms.CharField(
        label='Senha',
        min_length=8,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password'}
        ),
        error_messages={
            'required': 'Informe uma senha.',
            'min_length': 'A senha deve ter no mínimo 8 caracteres.',
        },
    )

    confirmar_senha = forms.CharField(
        label='Confirme a senha',
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password'}
        ),
        error_messages={
            'required': 'Confirme a senha.',
        },
    )

    def clean_senha(self):
        senha = self.cleaned_data['senha']

        if not (
            re.search(r'[A-Za-zÀ-ÿ]', senha)
            and re.search(r'\d', senha)
        ):
            raise forms.ValidationError(
                'A senha deve conter letras e números.'
            )

        return senha

    def clean(self):
        cleaned_data = super().clean()

        senha = cleaned_data.get('senha')
        confirmar = cleaned_data.get('confirmar_senha')

        if senha and confirmar and senha != confirmar:
            self.add_error(
                'confirmar_senha',
                'As senhas não são iguais.'
            )

        return cleaned_data
