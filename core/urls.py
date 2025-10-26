# core/urls.py

from django.urls import path
from . import views 
from .views import home, player_exibicao, tela_verificacao, gerenciar_midia, tela_login

urlpatterns = [
    # 1. HOME PAGE / DASHBOARD (URL raiz: http://127.0.0.1:8000/)
    path('', views.home, name='home'), 
    
    # 2. TELA DE VERIFICAÇÃO (Login do Dispositivo)
    path('verificar/', views.tela_verificacao, name='verificacao'), 

    # 3. PLAYER DE EXIBIÇÃO EM LOOP (Protegido pela verificação)
    path('exibir/', views.player_exibicao, name='player_exibicao'), 
    
    # 4. GERENCIAMENTO DE MÍDIA (Painel com HTMX)
    path('gerenciar/', views.gerenciar_midia, name='gerenciar_midia'),

    # 5. LOGIN DE VERIFICAÇÃO
    path('login/', views.tela_login, name='tela_login'),
]