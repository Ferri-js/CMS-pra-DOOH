# core/models/__init__.py

# Importa os Models de cada arquivo para que o Django os reconheça
from .dispositivo import Dispositivo
from .midia import Midia
from .playlist import Playlist
from .tipoDispositivo import TipoDispositivo
from .tipoMidia import tipoFormato
from .tipoStatus import tipoStatus
from .usuario import Usuario

# Importa a função de upload do Cloud
from .midia import cadastrarmidiaPcloud