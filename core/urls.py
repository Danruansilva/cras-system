from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cadastro/', views.cadastro_beneficiario, name='cadastro'),
    path('conceder-cesta/<int:beneficiario_id>/', views.conceder_cesta, name='conceder_cesta'),
    path('beneficiario/<int:beneficiario_id>/', views.detalhe_beneficiario, name='detalhe_beneficiario'),
    path('logout/', views.logout_view, name='logout'),
    path('excluir/<int:id>/', views.excluir_beneficiario, name='excluir_beneficiario'),
]
