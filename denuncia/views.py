from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect

from .models import Denuncia, ClassificacaoDenuncia, PROBLEMAS_POR_CATEGORIA
from .forms import DenunciaForm, SenhaDenunciaForm


def montar_setores(marcados):
    """Monta, para a etapa 1, a pergunta de cada setor (as perguntas do setor juntas)."""
    setores = []

    for tipo, nome in Denuncia.TIPO_DENUNCIA:
        perguntas = [
            f'{texto}?' for _valor, texto in PROBLEMAS_POR_CATEGORIA.get(tipo, [])
        ]
        setores.append({
            'valor': tipo,
            'nome': nome,
            'perguntas': perguntas,
            'sim': tipo in marcados,
        })

    return setores


def selecionar_setor(request):
    marcados = set()
    erro = None

    # Abrir a etapa 1 começa uma denúncia nova: descarta qualquer progresso anterior
    if request.method == 'GET':
        request.session.pop('setores', None)

    if request.method == 'POST':
        # Cada setor tem um campo "setor_<codigo>" com valor "sim" ou "nao"
        selecionados = [
            tipo for tipo, _nome in Denuncia.TIPO_DENUNCIA
            if request.POST.get(f'setor_{tipo}') == 'sim'
        ]
        marcados = set(selecionados)

        if selecionados:
            request.session['setores'] = selecionados
            return redirect('registro-denuncia')

        erro = 'Responda "Sim" em pelo menos uma pergunta para continuar.'

    return render(request, 'denuncia/setor.html', {
        'setores': montar_setores(marcados),
        'erro': erro,
    })


def registro(request):
    nomes_setores = dict(Denuncia.TIPO_DENUNCIA)

    # Mantém só setores que existem
    setores = [
        tipo for tipo in request.session.get('setores', [])
        if tipo in nomes_setores
    ]

    # Sem a etapa 1 concluída, volta para ela
    if not setores:
        return redirect('setor-denuncia')

    # O primeiro setor marcado é o setor principal da denúncia
    tipo_principal = setores[0]

    if request.method == 'POST':
        form = DenunciaForm(
            request.POST,
            request.FILES,
            instance=Denuncia(tipo=tipo_principal)
        )

        if form.is_valid():
            with transaction.atomic():
                denuncia = form.save()
                ClassificacaoDenuncia.objects.bulk_create([
                    ClassificacaoDenuncia(denuncia=denuncia, tipo=tipo)
                    for tipo in setores
                ])

            request.session['protocolo_recente'] = denuncia.protocolo
            request.session.pop('setores', None)

            return redirect('sucesso-denuncia', protocolo=denuncia.protocolo)
    else:
        form = DenunciaForm(instance=Denuncia(tipo=tipo_principal))

    return render(request, 'denuncia/registro.html', {
        'form': form,
        'nome_setor': ', '.join(nomes_setores[tipo] for tipo in setores),
    })


def cancelar(request):
    request.session.pop('setores', None)
    request.session.pop('protocolo_recente', None)
    return redirect('index-denuncia')


def index(request):
    # Página inicial pública
    return render(request, 'denuncia/index.html')

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