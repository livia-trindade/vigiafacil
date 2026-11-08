import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required

from .models import Denuncia, PROBLEMAS_POR_CATEGORIA
from .forms import DenunciaForm, SenhaDenunciaForm


def selecionar_setor(request):
    categorias = dict(Denuncia.TIPO_DENUNCIA)

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        problema = request.POST.get('problema')

        problemas_validos = dict(PROBLEMAS_POR_CATEGORIA.get(tipo, []))

        # Valida ambos antes de salvar na sessão e redirecionar
        if tipo in categorias and problema in problemas_validos:
            request.session['tipo'] = tipo
            request.session['problema'] = problema
            return redirect('registro-denuncia')

    # Converte tuplas para dicionário puro {tipo: [[chave, label], ...]}
    problemas_dict = {
        k: list(v) for k, v in PROBLEMAS_POR_CATEGORIA.items()
    }

    return render(request, 'denuncia/setor.html', {
        'categorias': Denuncia.TIPO_DENUNCIA,
        'problemas_json': json.dumps(problemas_dict),
    })


def registro(request):
    tipo = request.session.get('tipo')
    problema = request.session.get('problema')

    categorias = dict(Denuncia.TIPO_DENUNCIA)
    problemas_validos = dict(PROBLEMAS_POR_CATEGORIA.get(tipo, []))

    if tipo not in categorias or problema not in problemas_validos:
        return redirect('setor-denuncia')

    if request.method == 'POST':
        form = DenunciaForm(
            request.POST,
            request.FILES,
            instance=Denuncia(tipo=tipo, problema=problema)
        )

        if form.is_valid():
            denuncia = form.save()
            request.session['protocolo_recente'] = denuncia.protocolo
            request.session.pop('tipo', None)
            request.session.pop('problema', None)

            return redirect('sucesso-denuncia', protocolo=denuncia.protocolo)
    else:
        form = DenunciaForm(instance=Denuncia(tipo=tipo, problema=problema))

    return render(request, 'denuncia/registro.html', {
        'form': form,
        'nome_setor': categorias[tipo],
        'tipo_selecionado': tipo,
        'problema_selecionado': problema,
    })

@login_required
@permission_required('denuncia.view_denuncia', raise_exception=True)
def index(request):
    denuncias = Denuncia.objects.all()

    return render(request, 'denuncia/index.html', {
        'denuncias': denuncias
    })

def sucesso(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)

    # Só quem acabou de registrar vê esta tela e cadastra a senha.
    if request.session.get('protocolo_recente') != protocolo:
        return redirect('index-denuncia')

    senha_cadastrada = bool(denuncia.senha_hash)

    if request.method == 'POST' and not senha_cadastrada:
        form = SenhaDenunciaForm(request.POST)

        if form.is_valid():
            denuncia.definir_senha(form.cleaned_data['senha'])
            denuncia.save(update_fields=['senha_hash'])

            return redirect('sucesso-denuncia', protocolo=protocolo)

    else:
        form = SenhaDenunciaForm()

    return render(request, 'denuncia/sucesso.html', {
        'denuncia': denuncia,
        'form': form,
        'senha_cadastrada': senha_cadastrada,
    })


def acompanhar(request):
    denuncia = None
    erro = None

    if request.method == 'POST':
        protocolo = request.POST.get('protocolo', '').strip()
        senha = request.POST.get('senha', '')

        if not protocolo or not senha:
            erro = 'Informe o código do protocolo e a senha.'
        else:
            encontrada = Denuncia.objects.filter(protocolo=protocolo).first()

            if encontrada is None or not encontrada.conferir_senha(senha):
                erro = 'Protocolo ou senha incorretos.'
            else:
                denuncia = encontrada

    return render(request, 'denuncia/acompanhar.html', {
        'denuncia': denuncia,
        'erro': erro
    })
