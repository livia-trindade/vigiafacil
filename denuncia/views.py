
from django.shortcuts import render, get_object_or_404
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


def create(request):
    if request.method == 'POST':
        form = DenunciaForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/denuncia/sucesso/')
    else:
        form = DenunciaForm()

    return render(request, 'denuncia/create.html', {
        'form': form
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


def sucesso(request):
    return render(request, 'denuncia/sucesso.html')
