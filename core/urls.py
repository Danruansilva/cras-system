from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
 path('', views.home, name='home'),
    path('login/', views.home, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

   
    path('cadastro/', views.cadastro_beneficiario, name='cadastro'),
    path('conceder-cesta/<int:beneficiario_id>/', views.conceder_cesta, name='conceder_cesta'),
    path('excluir/<int:beneficiario_id>/', views.excluir_beneficiario, name='excluir'),
    path('detalhe/<int:beneficiario_id>/', views.detalhe_beneficiario, name='detalhe'),
]
