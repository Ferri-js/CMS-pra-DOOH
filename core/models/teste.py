from midia import Midia
from tipoStatus import tipoStatus
from playlist import Playlist
from datetime import date
from tipoMidia import tipoFormato
# Criando objetos de mídia
#midia1 = Midia(1, "teste", "Video", "https://www.youtube.com/watch?v=-UUjNRjuyu0", date.today(), tipoStatus.ATIVO, 6)
#midia2 = Midia(2, "teste2", "Video", "https://www.youtube.com/watch?v=lq_iZNHRnc4", date.today(), "Ativo", 10)
#midia3 = Midia(3, "teste3", "Foto", "https://tse2.mm.bing.net/th/id/OIP.U4X_DsaMGUaUqHtjMqUMmgHaEK?rs=1&pid=ImgDetMain&o=7&rm=3", date.today(), "Ativo", 0)

# Exemplo de mídia (supondo que 'tipo_midia_id' seja 1)

#elf, id, titulo, tipo, URL, dataUpload, status, duraca
midia1 = Midia(
    None,
    "Vídeo Teste",
    tipo= tipoFormato.JPEG,
    URL="abcd",
    dataUpload=date.today(),
    status = tipoStatus.ATIVO,
    duracao=120
)

# Adicionando atributo tipo_midia_id (obrigatório para FK)
#midia1.tipo_midia_id =  tipoFormato.MP4
#midia1.tamanho = None
#midia1.comprimento = None
midia1.largura = None


midia_id = midia1.cadastrarMidia()
print(f"Midia cadastrada com ID: {midia_id}")


# Criando uma playlist e adicionando mídias
playlist = Playlist(None, "Minha Playlist Teste")
playlist.adicionarMidia(midia1)

playlist_id = playlist.cadastrarPlaylist()
print(f"Playlist cadastrada com ID: {playlist_id}")
#play1.adicionarMidia(midia2)
#play1.adicionarMidia(midia3)


