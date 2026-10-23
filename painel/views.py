from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from denuncia.models import Denuncia
from .models import Acompanhamento
from .forms import StatusDenunciaForm, AcompanhamentoForm


@login_required
@permission_required('denuncia.view_denuncia', raise_exception=True)
def dashboard(request):
    denuncias = Denuncia.objects.all()

    return render(request, 'painel/dashboard.html', {
        'denuncias': denuncias
    })


@login_required
@permission_required('denuncia.view_denuncia', raise_exception=True)
def detalha(request, id_denuncia):
    denuncia = get_object_or_404(Denuncia, id=id_denuncia)
    acompanhamentos = denuncia.acompanhamentos.all()

    form_status = StatusDenunciaForm(instance=denuncia)
    form_acompanhamento = AcompanhamentoForm()

    return render(request, 'painel/detalha.html', {
        'denuncia': denuncia,
        'acompanhamentos': acompanhamentos,
        'form_status': form_status,
        'form_acompanhamento': form_acompanhamento
    })


@login_required
@permission_required('denuncia.change_denuncia', raise_exception=True)
def atualizar_status(request, id_denuncia):
    denuncia = get_object_or_404(Denuncia, id=id_denuncia)

    if request.method == 'POST':
        form = StatusDenunciaForm(request.POST, instance=denuncia)

        if form.is_valid():
            form.save()
            return redirect('detalha-painel', id_denuncia=denuncia.id)
    else:
        form = StatusDenunciaForm(instance=denuncia)

    return render(request, 'painel/atualizar_status.html', {
        'denuncia': denuncia,
        'form': form
    })


@login_required
@permission_required('painel.add_acompanhamento', raise_exception=True)
def registrar_acompanhamento(request, id_denuncia):
    denuncia = get_object_or_404(Denuncia, id=id_denuncia)

    if request.method == 'POST':
        form = AcompanhamentoForm(request.POST)

        if form.is_valid():
            acompanhamento = form.save(commit=False)
            acompanhamento.denuncia = denuncia
            acompanhamento.vigilante = request.user
            acompanhamento.save()

            return redirect('detalha-painel', id_denuncia=denuncia.id)
    else:
        form = AcompanhamentoForm()

    return render(request, 'painel/acompanhamento.html', {
        'denuncia': denuncia,
        'form': form
    })