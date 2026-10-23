from django import forms
from denuncia.models import Denuncia
from .models import Acompanhamento


class StatusDenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['status']


class AcompanhamentoForm(forms.ModelForm):
    class Meta:
        model = Acompanhamento
        fields = ['descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva as providências tomadas...'
            })
        }