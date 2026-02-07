from django.urls import path
from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    # 🔑 LOGIN
    path('login/', views.home, name='login'),

     path('excluir/<int:id>/', views.excluir_beneficiario, name='excluir_beneficiario'),

    # 📊 DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    # 📝 CADASTRO
    path('cadastro/', views.cadastro_beneficiario, name='cadastro'),

    # 🧺 CONCEDER CESTA
    path('conceder-cesta/<int:beneficiario_id>/', views.conceder_cesta, name='conceder_cesta'),

    # 👁 DETALHE DO BENEFICIÁRIO
    path('beneficiario/<int:beneficiario_id>/', views.detalhe_beneficiario, name='detalhe_beneficiario'),

    # 🚪 LOGOUT
    path('logout/', views.logout_view, name='logout'),

     path('', include('core.urls')),

    path(
    'excluir-beneficiario/<int:beneficiario_id>/',
    views.excluir_beneficiario,
    name='excluir_beneficiario'
),

       path('', views.dashboard, name='dashboard'),
    path('beneficiario/excluir/<int:beneficiario_id>/', views.excluir_beneficiario, name='excluir_beneficiario'),
    # outras rotas aqui

]
