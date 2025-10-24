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
from core.models.disp_playlist import Dispositivo_Playlist
from core.models.midia_playlist import Midia_Playlist


tipoMidia1 = tipoFormato.objects.get(id=2)
tipoMidia2 = tipoFormato.objects.get(id=2)
tipoMidia3 = tipoFormato.objects.get(id=1)
tipoMidia4 = tipoFormato.objects.get(id=2)

midia1 = Midia(
    titulo="Praying 1",
    tipo_midia=tipoMidia1,
    url="https://static.wikia.nocookie.net/liberproeliis/images/7/7b/Fd371d211c8318a3cc5fcab6e34ea59a.jpg/revision/latest/scale-to-width-down/600?cb=20170313174539&path-prefix=pt-br",
    status= tipoStatus.ATIVO.value,
    duracao=90,
    data_upload=timezone.now()
)

midia2 = Midia(
    titulo="Crash 2",
    tipo_midia=tipoMidia2,
    url="https://u.pcloud.link/publink/show?code=XZ5T6n5ZRIjFNQRW4ouI6CqywkhpTRVePQJ7",
    status= tipoStatus.ATIVO.value,
    duracao=90,
    data_upload=timezone.now()
)

midia3 = Midia(
    titulo="Crash 3",
    tipo_midia=tipoMidia3,
    url="https://u.pcloud.link/publink/show?code=XZJT6n5ZU5bywmrzSPSmBASTpE1NCXxphOP7",
    status= tipoStatus.ATIVO.value,
    duracao=90,
    data_upload=timezone.now()
)

midia4 = Midia(
    titulo="Crash 4",
    tipo_midia=tipoMidia4,
    url="https://u.pcloud.link/publink/show?code=XZFT6n5ZXzYqDXgPfnF90zTddHVOwBat0b4y",
    status= tipoStatus.ATIVO.value,
    duracao=90,
    data_upload=timezone.now()
)

#Midia.cadastrarMidiaPcloud()


tipoDisp = TipoDispositivo.objects.get(id=1)

disp = Dispositivo(
    nomeDispositivo='Dispositivo Back end e Front end integrado',
    status = tipoStatus.ATIVO.value,
    codVerificacao= 'nextage',
    tipoDispositivo = tipoDisp
)

play = Playlist(
    nomePlaylist='playlist teste frontend'
)


play.cadastrarPlaylistORM()
#print(f"Playlist criada/atualizada com ID: {play.idPlaylist}")

#disp.cadastrarDispositivoORM()
#print(f"Dispositivo criado/atualizado com ID: {disp.idDispositivo}")



#midia1.cadastrarMidia()
#print(f"Mídia criada/atualizada com ID: {midia1.id}")


#midia2.cadastrarMidia()
#print(f"Mídia criada/atualizada com ID: {midia2.id}")


#midia3.cadastrarMidia()
#print(f"Mídia criada/atualizada com ID: {midia3.id}")


#midia4.cadastrarMidia()
#print(f"Mídia criada/atualizada com ID: {midia4.id}")
#midia1.save()
#midia2.save()
#midia3.save()
#midia4.save()
#play.save()

mp1 = Midia_Playlist(
    id_midia = midia1,
    id_playlist = play,
    ordem_midia = 1,
)

mp2 = Midia_Playlist(
    id_midia = midia2,
    id_playlist = play,
    ordem_midia = 2,
)

mp3 = Midia_Playlist(
    id_midia = midia3,
    id_playlist = play,
    ordem_midia = 3,
)

mp4 = Midia_Playlist(
    id_midia = midia4,
    id_playlist = play,
    ordem_midia = 4,
)

#mp1.associarMP()
#mp2.associarMP()
#mp3.associarMP()
#mp4.associarMP()


disPlaylist = Dispositivo_Playlist(
    id_playlist = play,
    id_dispositivo = disp,
    ordem_playlist = 1
)

disp.cadastrarDispositivoORM()

disPlaylist.associarDispPlay()
#print(f"Playlist associada a dispositivo com id: {disPlaylist.id}")

#print(f"Mídia associada a playlist com ID_MP: {mp1.id_MP}")

#Midia.cadastrarMidiaSupabase()