import os
import django
from datetime import datetime
from django.utils import timezone
# Configure o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexxo_cms.settings')  # Substitua corretamente
django.setup()

# Agora os imports funcionam como em qualquer lugar do projeto
from core.models.tipoMidia import tipoFormato
from core.models.midia import Midia
from core.models.dispositivo import Dispositivo
from core.models.tipoDispositivo import TipoDispositivo
from core.models.tipoStatus import tipoStatus
from core.models.playlist import Playlist


tipo = tipoFormato.objects.get(id=1)

midia = Midia(
    titulo="Teste direto do script",
    tipo_midia=tipo,
    url="http://exemplo.com/scriptABCDE",
    status= tipoStatus.ATIVO.value,
    duracao=90,
    data_upload=timezone.now()
)


tipoDisp = TipoDispositivo.objects.get(id=1)

disp = Dispositivo(
    nomeDispositivo='Dispositivo TESTE ORM STATUS',
    status = tipoStatus.ATIVO.value,
    codVerificacao= 'abc1',
    tipoDispositivo = tipoDisp
)

play = Playlist(
    nomePlaylist='Playlist teste via ORM'
)


play.cadastrarPlaylistORM()
print(f"Playlist criada/atualizada com ID: {play.idPlaylist}")

disp.cadastrarDispositivoORM()
print(f"Dispositivo criado/atualizado com ID: {disp.idDispositivo}")



#midia.cadastrarMidia()
#print(f"Mídia criada/atualizada com ID: {midia.id}")

