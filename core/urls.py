from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.home, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('cadastro/', views.cadastro_beneficiario, name='cadastro'),

    path(
        'beneficiario/<int:beneficiario_id>/',
        views.detalhe_beneficiario,
        name='detalhe_beneficiario'
    ),

    path(
        'conceder-cesta/<int:beneficiario_id>/',
        views.conceder_cesta,
        name='conceder_cesta'
    ),

    path(
        'excluir/<int:beneficiario_id>/',
        views.excluir_beneficiario,
        name='excluir_beneficiario'
    ),

    path(
        'requerimento-beneficio/',
        views.requerimento_beneficio,
        name='requerimento_beneficio'
    ),
    path(
    'requerimento/',
    views.lista_beneficiarios_requerimento,
    name='requerimento_beneficio'
),

]
