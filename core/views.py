from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Q, Count
from .models import Beneficiario
from django.http import HttpResponse
def home(request):
    return HttpResponse("Sistema CRAS está online 🚀")

def home(request):
    """Tela de login"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')


    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('core:dashboard')


    return render(request, 'core/login.html', {'form': form})

@login_required
def excluir_beneficiario(request, beneficiario_id):
    beneficiario = get_object_or_404(Beneficiario, id=beneficiario_id)
    beneficiario.delete()
    return redirect('core:dashboard')


@login_required
def cadastro_beneficiario(request):
    """Cadastrar novo beneficiário"""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')

        try:
            Beneficiario.objects.create(
                nome=nome,
                cpf=cpf
            )
            messages.success(request, 'Beneficiário cadastrado com sucesso!')
            return redirect('dashboard')
        except IntegrityError:
            messages.error(request, 'Este CPF já está cadastrado.')

    return render(request, 'core/cadastro.html')


@login_required
def dashboard(request):
    """Dashboard com pesquisa e lista de beneficiários"""
    busca = request.GET.get('q', '').strip()

    # Busca beneficiários com total de cestas
    beneficiarios = Beneficiario.objects.annotate(
        total_cestas=Count('cestas')
    )

    if busca:
        beneficiarios = beneficiarios.filter(
            Q(nome__icontains=busca) |
            Q(cpf__icontains=busca)
        )
        encontrado = beneficiarios.exists()
    else:
        encontrado = True

    context = {
        'beneficiarios': beneficiarios,
        'busca': busca,
        'encontrado': encontrado
    }

    return render(request, 'core/dashboard.html', context)


@login_required
def conceder_cesta(request, beneficiario_id):
    """Concede cesta para o beneficiário se permitido"""
    beneficiario = get_object_or_404(Beneficiario, id=beneficiario_id)

    pode, msg = beneficiario.pode_receber_cesta()

    if pode:
        beneficiario.conceder_cesta()
        messages.success(request, f"Cesta concedida para {beneficiario.nome}!")
    else:
        messages.error(request, f"Não foi possível conceder cesta: {msg}")

    return HttpResponseRedirect(reverse('dashboard'))


@login_required
def detalhe_beneficiario(request, beneficiario_id):
    """Detalhes individuais do beneficiário"""
    beneficiario = get_object_or_404(Beneficiario, id=beneficiario_id)
    return render(
        request,
        'core/detalhe_beneficiario.html',
        {'beneficiario': beneficiario}
    )


@login_required
def logout_view(request):
    """Logout do usuário"""
    logout(request)
    return redirect('login')
