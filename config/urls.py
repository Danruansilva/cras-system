from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin do Django
    path('admin/', admin.site.urls),

    # Todas as URLs do app 'core'
    path('', include('core.urls')),  # todas as rotas do core serão gerenciadas aqui
]
