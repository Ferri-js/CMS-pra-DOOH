# core/admin.py

from django.contrib import admin
# Importe TODOS os Models que você quer gerenciar
from .models import Midia, Playlist, ItemPlaylist, Dispositivo, TipoDispositivo 

# --- 1. CONFIGURAÇÃO PARA MIDIA (COM SEARCH_FIELDS) ---
@admin.register(Midia)
class MidiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'url_publica', 'status', 'data_upload', 'duracao')
    list_filter = ('tipo', 'status')
    # ⬇️ ESSENCIAL para o autocomplete funcionar no ItemPlaylistInline
    search_fields = ('titulo', 'url_publica') 
    
# --- 2. REGISTRO SIMPLES ---
# Registra TipoDispositivo para gerenciamento básico
admin.site.register(TipoDispositivo)

# --- 3. REGISTRO CUSTOMIZADO PARA PLAYLIST (Com Itens na mesma tela) ---
class ItemPlaylistInline(admin.TabularInline):
    model = ItemPlaylist
    extra = 1 # Mostra um campo extra para adicionar um novo item
    fields = ('midia', 'ordem')
    # ⬇️ Esta linha agora funciona porque MidiaAdmin tem search_fields
    autocomplete_fields = ('midia',) 

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativa') # Campos visíveis na lista de playlists
    list_filter = ('ativa',) # Filtro lateral para playlists ativas/inativas
    # ⬇️ ESSENCIAL para o autocomplete funcionar no DispositivoAdmin
    search_fields = ('titulo',) 
    inlines = [ItemPlaylistInline] # Permite editar os itens da playlist na mesma tela

# --- 4. REGISTRO CUSTOMIZADO PARA DISPOSITIVO ---
@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ('nomeDispositivo', 'tipoDispositivo', 'codVerificacao', 'status', 'playlistAssociada') # Campos na lista
    list_filter = ('tipoDispositivo', 'status') # Filtros laterais
    search_fields = ('nomeDispositivo', 'codVerificacao') # Campos para busca
    
    # Define os campos que aparecerão no formulário de edição do dispositivo
    fields = ('nomeDispositivo', 'tipoDispositivo', 'codVerificacao', 'status', 'playlistAssociada')
    
    # ⬇️ Facilita a seleção da Playlist se houver muitas (Funciona porque PlaylistAdmin tem search_fields)
    autocomplete_fields = ('playlistAssociada',)