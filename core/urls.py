# core/urls.py

from django.urls import path
#from . import views # <-- Importa o pacote views (que agora tem um __init__.py corrigido)
#from core.views import home
from core.views import dispositivo_view, player_view, gerenciar_midia
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
      path('gerenciar/', gerenciar_midia, name='gerenciar_midia'), 
]

