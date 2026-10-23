from .models import Denuncia
from django.forms import ModelForm

class DenunciaForm(ModelForm):
    class Meta:
        model = Denuncia
        fields = [
            'tipo',
            'descricao',
            'endereco',
            'bairro',
            'data_ocorrencia',
        ]