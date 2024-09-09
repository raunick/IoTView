from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('monitoramento/', include('monitoramento.urls')),
    path('seguranca/', include('seguranca.urls')),
    path('relatorio/', include('relatorio.urls')),
]
