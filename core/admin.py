from django.contrib import admin
from .models import Midia, Playlist, ItemPlaylist # Importe os models de playlist

# Model de Mídia (Uploads)
admin.site.register(Midia)

# O restante do código da Playlist foi removido temporariamente, 
# pois ele estava causando o erro, já que 'ItemPlaylist' e 'Playlist' 
# não são Models válidos do Django.
# core/admin.py
# ... (Model Midia já está registrado)

# Adicione estes comandos para ver as playlists no admin:
admin.site.register(Playlist)
admin.site.register(ItemPlaylist)