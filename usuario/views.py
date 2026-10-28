from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from .models import Usuario
from .forms import UsuarioForm, UsuarioEditForm


def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)
                return redirect('dashboard-painel')

        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'usuario/login.html')


@login_required
def logout_usuario(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login-usuario')

    return render(request, 'usuario/logout.html')


@login_required
@permission_required('usuario.add_usuario', raise_exception=True)
def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('listar-usuarios')
    else:
        form = UsuarioForm()

    return render(request, 'usuario/criar.html', {
        'form': form
    })


@login_required
@permission_required('usuario.view_usuario', raise_exception=True)
def listar_usuarios(request):
    usuarios = Usuario.objects.all()

    return render(request, 'usuario/listar.html', {
        'usuarios': usuarios
    })


@login_required
@permission_required('usuario.view_usuario', raise_exception=True)
def detalhar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)

    return render(request, 'usuario/detalhar.html', {
        'usuario': usuario
    })


@login_required
@permission_required('usuario.change_usuario', raise_exception=True)
def editar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)

    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('listar-usuarios')
    else:
        form = UsuarioEditForm(instance=usuario)

    return render(request, 'usuario/editar.html', {
        'form': form,
        'usuario': usuario
    })


@login_required
@permission_required('usuario.delete_usuario', raise_exception=True)
def excluir_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('listar-usuarios')

    return render(request, 'usuario/excluir.html', {
        'usuario': usuario
    })