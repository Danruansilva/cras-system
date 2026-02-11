from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),  # Página inicial = login
    path('dashboard/', views.dashboard, name='dashboard'),

    path('login/', views.home, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
