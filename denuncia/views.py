from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Denuncia, PROBLEMAS_POR_CATEGORIA
from .forms import DenunciaForm, SenhaDenunciaForm


@login_required
@permission_required('denuncia.view_denuncia', raise_exception=True)
def index(request):
    denuncias = Denuncia.objects.all()
    return render(request, 'denuncia/index.html', {
        'denuncias': denuncias
    })
CATEGORIA_PADRAO = 'outro'
PROBLEMA_PADRAO = 'outro_problema'


def registro(request):
    # Quando a etapa 1 existir, ela vai enviar ?tipo=...&problema=...
    tipo = request.GET.get('tipo')
    problema = request.GET.get('problema')

    if tipo and problema:
        request.session['tipo'] = tipo
        request.session['problema'] = problema

    tipo = request.session.get('tipo', CATEGORIA_PADRAO)
    problema = request.session.get('problema', PROBLEMA_PADRAO)

    categorias = dict(Denuncia.TIPO_DENUNCIA)
    problemas = dict(PROBLEMAS_POR_CATEGORIA.get(tipo, []))


    if tipo not in categorias or problema not in problemas:
        tipo = CATEGORIA_PADRAO
        problema = PROBLEMA_PADRAO

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

            return redirect(
                'sucesso-denuncia',
                protocolo=denuncia.protocolo
            )
    else:
        form = DenunciaForm(
            instance=Denuncia(tipo=tipo, problema=problema)
        )

    return render(request, 'denuncia/registro.html', {
        'form': form,
        'nome_setor': categorias[tipo],
    })


def sucesso(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)

    # Só quem acabou de registrar vê esta tela e cadastra a senha
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

