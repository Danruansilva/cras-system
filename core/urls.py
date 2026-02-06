from django.urls import path
from . import views

urlpatterns = [
    # 🔑 LOGIN
    path('login/', views.home, name='login'),

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
]
