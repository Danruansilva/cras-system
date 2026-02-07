from django.urls import path
from core import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cadastro/', views.cadastro_beneficiario, name='cadastro'),
    path('conceder_cesta/<int:beneficiario_id>/', views.conceder_cesta, name='conceder_cesta'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
     path('admin/', admin.site.urls),
    path('', include('core.urls')),  # ← só incluir APPs aqui
    
]
