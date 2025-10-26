# core/urls.py

from django.urls import path
from . import views 

urlpatterns = [
    # 1. HOME PAGE / DASHBOARD (URL raiz: /)
    path('', views.home, name='home'), 
    
    # 2. TELA DE VERIFICAÇÃO (Login do Dispositivo)
    path('verificar/', views.tela_verificacao, name='verificacao'), 

    # 3. PLAYER DE EXIBIÇÃO EM LOOP (Protegido pela verificação)
    path('exibir/', views.player_exibicao, name='player_exibicao'), 
    
    # 4. GERENCIAMENTO DE MÍDIA (Painel com HTMX, protegido por login)
    path('gerenciar/', views.gerenciar_midia, name='gerenciar_midia'),
    
    # 5. TELA DE LOGIN CUSTOMIZADA
    path('login/', views.tela_login, name='tela_login'),
]