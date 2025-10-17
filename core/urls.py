# core/urls.py

from django.urls import path
from . import views # <-- Importa o pacote views (que agora tem um __init__.py corrigido)

urlpatterns = [
    path('', views.home, name='home'),
    path('gerenciar/', views.gerenciar_midia, name='gerenciar_midia'), 
]