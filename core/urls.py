# core/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    # 1. HOME PAGE / DASHBOARD (O "Seja Bem-vindo")
    path('', views.home, name='home'), 
    
    # 2. LOGIN / LOGOUT / VERIFICAÇÃO
    path('login/', views.tela_login, name='tela_login'),
    path('logout/', views.tela_logout, name='logout'),
    path('verificar/', views.tela_verificacao, name='verificacao'), 

    # 3. PLAYER
    path('exibir/', views.player_exibicao, name='player_exibicao'), 
    
    # 4. PAINEL DE GERENCIAMENTO (O PAINEL VISUAL)
    # A URL principal do painel (GET)
    path('gerenciar/', views.painel_gerenciamento, name='painel_gerenciamento'),
    
    # 5. URLs DO HTMX (para o painel de gerenciamento)
    
    # --- Mídias ---
    path('htmx/upload-midia/', views.upload_midia, name='upload_midia'),
    path('htmx/lista-midias/', views.lista_midias, name='lista_midias'),

    # --- Playlists ---
    path('htmx/criar-playlist/', views.criar_playlist, name='criar_playlist'),
    path('htmx/lista-playlists/', views.lista_playlists, name='lista_playlists'),
    
    # --- Itens da Playlist (Detalhes) ---
    path('htmx/detalhe-playlist/<int:playlist_id>/', views.detalhe_playlist, name='detalhe_playlist'),
    path('htmx/adicionar-item/<int:playlist_id>/', views.adicionar_item_playlist, name='adicionar_item_playlist'),
    path('htmx/remover-item/<int:item_id>/', views.remover_item_playlist, name='remover_item_playlist'),

    # --- Dispositivos ---
    path('htmx/criar-dispositivo/', views.criar_dispositivo, name='criar_dispositivo'),
    path('htmx/lista-dispositivos/', views.lista_dispositivos, name='lista_dispositivos'),
    path('htmx/detalhe-dispositivo/<int:dispositivo_id>/', views.detalhe_dispositivo, name='detalhe_dispositivo'),
    path('htmx/editar-dispositivo/<int:dispositivo_id>/', views.editar_dispositivo, name='editar_dispositivo'),
]