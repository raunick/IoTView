from django.urls import path
from . import views

urlpatterns = [
    path('', views.gerenciar_seguranca, name='gerenciar_seguranca'),
]
