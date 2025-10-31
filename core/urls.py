# core/urls.py

from django.urls import path
<<<<<<< HEAD
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
=======
from .views import home
from core.views.teste_frontend import teste_frontend 
from core.views.upload_midia import upload_midia
from core.views.codVerificacao import dispositivo_view
from core.views.player_web import player_view

urlpatterns = [
      path('', home, name='home'),
      path('teste_frontend/', teste_frontend, name='teste_frontend'),
      path('upload/', upload_midia, name='upload_midia'),
      path('dispositivo/<str:codigo>', dispositivo_view, name='disp_player'),
      path('dispositivo/<str:codigo>/player', player_view, name='player'),
]
>>>>>>> 8c61ace3cb8eb645de17337dedd848e18d3ba571
