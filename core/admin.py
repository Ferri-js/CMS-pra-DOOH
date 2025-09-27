from django.contrib import admin
from .models import Midia, Playlist, ItemPlaylist

# Model de Mídia (Uploads)
admin.site.register(Midia)

# Permite adicionar Itens da Playlist diretamente na página da Playlist
class ItemPlaylistInline(admin.TabularInline):
    model = ItemPlaylist
    extra = 1

# ModelAdmin para a Playlist
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativa')
    inlines = [ItemPlaylistInline]