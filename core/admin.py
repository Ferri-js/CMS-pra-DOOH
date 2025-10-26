from django.contrib import admin
from .models import Midia, Playlist, ItemPlaylist, Dispositivo, TipoDispositivo 

# --- 1. REGISTRO DE MODELS SIMPLES ---
admin.site.register(Midia)
admin.site.register(TipoDispositivo)
admin.site.register(Dispositivo) # AGORA ESTA LINHA VAI FUNCIONAR


# --- 2. REGISTRO DE PLAYLISTS (INLINES) ---
class ItemPlaylistInline(admin.TabularInline):
    model = ItemPlaylist
    extra = 1 
    fields = ('midia', 'ordem') 
    raw_id_fields = ('midia',) 

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativa')
    list_filter = ('ativa',)
    inlines = [ItemPlaylistInline]