from django.urls import path
from . import views

urlpatterns = [
    path('', views.gerar_relatorio, name='gerar_relatorio'),
]
