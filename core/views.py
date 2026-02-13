from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Max, Q
from .models import Beneficiario, Cesta


def home(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if 'next' in request.GET:
        messages.warning(request, "Faça login primeiro.")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('core:dashboard')

    return render(request, 'core/login.html', {'form': form})


@login_required(login_url='core:login')
def dashboard(request):
    busca = request.GET.get('q', '')

    beneficiarios = Beneficiario.objects.annotate(
        total_cestas_calc=Count('cestas'),
        data_ultima_cesta=Max('cestas__data_concessao')
    ).order_by('nome')

    if busca:
        beneficiarios = beneficiarios.filter(
            Q(nome__icontains=busca) |
            Q(cpf__icontains=busca)
        )

    return render(request, 'core/dashboard.html', {
        'beneficiarios': beneficiarios,
        'busca': busca,
    })


@login_required(login_url='core:login')
def cadastro_beneficiario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        rg = request.POST.get('rg')
        endereco = request.POST.get('endereco')

        recebe_beneficio = request.POST.get('recebe_beneficio') == 'sim'
        qual_beneficio = request.POST.get('qual_beneficio')
        documento_foto = request.FILES.get('documento_foto')

        try:
            Beneficiario.objects.create(
                nome=nome,
                cpf=cpf,
                rg=rg,
                endereco=endereco,
                recebe_beneficio=recebe_beneficio,
                qual_beneficio=qual_beneficio if recebe_beneficio else None,
                documento_foto=documento_foto
            )
            messages.success(request, 'Beneficiário cadastrado com sucesso!')
            return redirect('core:dashboard')

        except IntegrityError:
            messages.error(request, 'Este CPF já está cadastrado.')

    return render(request, 'core/cadastro.html')


@login_required(login_url='core:login')
def conceder_cesta(request, beneficiario_id):
    if request.method != 'POST':
        return redirect('core:dashboard')

    beneficiario = get_object_or_404(Beneficiario, id=beneficiario_id)

    pode, msg = beneficiario.pode_receber_cesta()

    if pode:
        beneficiario.conceder_cesta()
        messages.success(request, f'Cesta concedida para {beneficiario.nome}!')
    else:
        messages.error(request, msg)

    return redirect('core:dashboard')


@login_required(login_url='core:login')
def excluir_beneficiario(request, beneficiario_id):
    beneficiario = get_object_or_404(Beneficiario, id=beneficiario_id)
    beneficiario.delete()
    messages.success(request, 'Beneficiário excluído com sucesso!')
    return redirect('core:dashboard')


@login_required(login_url='core:login')
def detalhe_beneficiario(request, beneficiario_id):
    beneficiario = get_object_or_404(Beneficiario, id=beneficiario_id)

    cestas = beneficiario.cestas.order_by('-data_concessao')

    is_pdf = False
    if beneficiario.documento_foto:
        try:
            url = beneficiario.documento_foto.url
            is_pdf = url.lower().endswith('.pdf')
        except Exception:
            is_pdf = False

    return render(
        request,
        'core/detalhe_beneficiario.html',
        {
            'beneficiario': beneficiario,
            'cestas': cestas,
            'is_pdf': is_pdf
        }
    )


@login_required(login_url='core:login')
def logout_view(request):
    logout(request)
    return redirect('core:home')
