
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Denuncia
from .forms import DenunciaForm


@login_required
@permission_required('denuncia.view_denuncia', raise_exception=True)
def index(request):
    denuncias = Denuncia.objects.all()
    return render(request, 'denuncia/index.html', {
        'denuncias': denuncias
    })


@login_required
@permission_required('denuncia.view_denuncia', raise_exception=True)
def detalha(request, id_denuncia):
    denuncia = get_object_or_404(Denuncia, id=id_denuncia)
    return render(request, 'denuncia/detalha.html', {
        'denuncia': denuncia
    })


def registro(request):
    if request.method == 'POST':
        form = DenunciaForm(request.POST)

        if form.is_valid():
            denuncia = form.save()
            return redirect(
                'sucesso-denuncia',
                protocolo=denuncia.protocolo
            )
    else:
        form = DenunciaForm()

    return render(request, 'denuncia/registro.html', {
        'form': form
    })


def sucesso(request, protocolo):
    denuncia = get_object_or_404(
        Denuncia,
        protocolo=protocolo
    )

    return render(request, 'denuncia/sucesso.html', {
        'denuncia': denuncia
    })

def acompanhar(request):
    denuncia = None
    erro = None

    if request.method == 'POST':
        protocolo = request.POST.get('protocolo', '').strip()

        if protocolo:
            denuncia = Denuncia.objects.filter(
                protocolo=protocolo
            ).only('protocolo', 'status').first()

            if denuncia is None:
                erro = 'Nenhuma denúncia foi encontrada com esse protocolo.'
        else:
            erro = 'Informe o código do protocolo.'

    return render(request, 'denuncia/acompanhar.html', {
        'denuncia': denuncia,
        'erro': erro
    })

@login_required
@permission_required('denuncia.change_denuncia', raise_exception=True)
def update(request, id_denuncia):
    denuncia = get_object_or_404(Denuncia, id=id_denuncia)

    if request.method == 'POST':
        form = DenunciaForm(request.POST, instance=denuncia)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/denuncia/')
    else:
        form = DenunciaForm(instance=denuncia)

    return render(request, 'denuncia/update.html', {
        'form': form,
        'denuncia': denuncia
    })


@login_required
@permission_required('denuncia.delete_denuncia', raise_exception=True)
def delete(request, id_denuncia):
    denuncia = get_object_or_404(Denuncia, id=id_denuncia)

    if request.method == 'POST':
        denuncia.delete()
        return HttpResponseRedirect('/denuncia/')

    return render(request, 'denuncia/delete.html', {
        'denuncia': denuncia
    })
