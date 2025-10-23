# core/models/__init__.py

from .midia import Midia # <-- Isso lista o Model Midia

# ⬇️ ADICIONE ESTA LINHA (Assumindo que PlaylistDB está em playlist.py)
from .playlist import Playlist, ItemPlaylist

from .tipoDispositivo import TipoDispositivo 