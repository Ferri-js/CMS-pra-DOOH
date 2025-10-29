# core/models/__init__.py

from .midia import Midia # <-- Isso lista o Model Midia

# ⬇️ ADICIONE ESTA LINHA (Assumindo que PlaylistDB está em playlist.py)
from .playlist import Playlist

from .tipoDispositivo import TipoDispositivo 

from .midia_playlist import Midia_Playlist

from .dispositivo import Dispositivo

from .disp_playlist import Dispositivo_Playlist