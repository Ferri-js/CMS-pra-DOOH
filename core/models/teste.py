from midia import Midia
from playlist import Playlist
#from models.teste import midia_remover
from datetime import date, datetime, timezone
from tipoMidia import tipoFormato
from tipoStatus import tipoStatus
from dispositivo import Dispositivo  # supondo que você salvou a classe em dispositivo.py
from tipoDispositivo import TipoDispositivo  # enum que você criou

#midia1 = Midia(1, "teste", "Video", "https://www.youtube.com/watch?v=-UUjNRjuyu0", date.today(), tipoStatus.ATIVO, 6)
#midia2 = Midia(2, "teste2", "Video", "https://www.youtube.com/watch?v=lq_iZNHRnc4", date.today(), "Ativo", 10)
#midia3 = Midia(3, "teste3", "Foto", "https://tse2.mm.bing.net/th/id/OIP.U4X_DsaMGUaUqHtjMqUMmgHaEK?rs=1&pid=ImgDetMain&o=7&rm=3", date.today(), "Ativo", 0)

#midia1 = Midia(
#    None,
#    "Vídeo Teste",
#    tipo= tipoFormato.JPEG,
#    URL="youtube.com",
#    dataUpload=date.today(),
#    status = tipoStatus.ATIVO,
#    duracao=120
#)


#midia_id = midia1.cadastrarMidia()
#print(f"Midia cadastrada com ID: {midia_id}")


# Criando uma playlist e adicionando mídias
#playlist = Playlist(None, "Minha Playlist Teste")
#playlist.adicionarMidia(midia1)

#playlist_id = playlist.cadastrarPlaylist()
#print(f"Playlist cadastrada com ID: {playlist_id}")
#play1.adicionarMidia(midia2)
#play1.adicionarMidia(midia3)

# agora pode usar direto
tipo = tipoFormato.objects.get(id=1)  # pega o tipo que já existe
m = Midia(
    titulo="Vídeo de teste",
    tipo_midia=tipo,
    url="http://teste.com/video1Teste",
    status="ativo",
    duracao=300,
    data_upload=timezone.now()
)

m.cadastrarMidia()

#midia1.cadastrarMidiaPcloud()
#Midia.cadastrarMidiaPcloud()

#play1 = Playlist(1, "TesteP")

#play1.adicionarMidia(midia1)
#play1.adicionarMidia(midia2)
#play1.adicionarMidia(midia3)

#play1.abrirPlaylist()


#midia1.removerMidia();

#midia_remover.removerMidia()


# Criação do objeto
dispositivo = Dispositivo(
    idDispositivo=100,                     # ID personalizado (pode ser None se for AUTO_INCREMENT)
    nomeDispositivo="Smart TV Samsung",
    tipoDispositivo=TipoDispositivo.VIDEO_WALL,
    armazenamento=128,
    status="ativo",
    comprimento=120,
    largura=70,
    cod_verificacao="abc123xyz"
)

# Inserção no banco
try:
    dispositivo_id = dispositivo.cadastrarDispositivo()
    if dispositivo_id:
        print(f"✅ Dispositivo inserido com ID: {dispositivo_id}")
    else:
        print("⚠️ Dispositivo já existe no banco de dados.")
except Exception as e:
    print("❌ Erro ao inserir dispositivo:", e)