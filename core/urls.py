# core/urls.py

from django.urls import path
#from . import views # <-- Importa o pacote views (que agora tem um __init__.py corrigido)
#from core.views import home
from core.views import dispositivo_view, player_view, gerenciar_midia, gerenciar_disp
from core.views import gerenciar_playlist, gerenciar_mp, gerenciar_disp_play
#from core.views.teste_frontend import teste_frontend 
#from core.views.upload_midia import upload_midia
#from core.views.codVerificacao import dispositivo_view
#from core.views.player_web import player_view

urlpatterns = [
  #    path('', home, name='home'),
 #     path('teste_frontend/', teste_frontend, name='teste_frontend'),
 #     path('upload/', views.upload_midia, name='upload_midia'),
      path('dispositivo/<str:codigo>', dispositivo_view, name='disp_player'),
      path('dispositivo/<str:codigo>/player', player_view, name='player'),
      path('gerenciar_midia/', gerenciar_midia, name='gerenciar_midia'),
      path('gerenciar_play/', gerenciar_playlist, name='gerenciar_play'),  
      path('gerenciar_mp/<int:playlist_id>/', gerenciar_mp, name='gerenciar_mp'),
      path('gerenciar_mp/<int:playlist_id>/<int:midia_id>/', gerenciar_mp, name='gerenciar_mp'),
      path('gerenciar_disp/', gerenciar_disp, name='gerenciar_disp'),
      path('gerenciar_disp/play/<int:dispositivo_id>/', gerenciar_disp_play, name='gerenciar_disp_play'),
      path('gerenciar_disp/play/<int:dispositivo_id>/<int:playlist_id>/', gerenciar_disp_play, name='gerenciar_disp_play'),
]

