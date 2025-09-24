from midia import Midia
from playlist import Playlist
from datetime import date
# agora pode usar direto
midia1 = Midia(1, "teste", "Video", "https://www.youtube.com/watch?v=-UUjNRjuyu0", date.today(), "Ativo", 6)
midia2 = Midia(2, "teste2", "Video", "https://www.youtube.com/watch?v=lq_iZNHRnc4", date.today(), "Ativo", 10)
midia3 = Midia(3, "teste3", "Foto", "https://tse2.mm.bing.net/th/id/OIP.U4X_DsaMGUaUqHtjMqUMmgHaEK?rs=1&pid=ImgDetMain&o=7&rm=3", date.today(), "Ativo", 0)
#midia1.exibirMidia()


play1 = Playlist(1, "TesteP")

play1.adicionarMidia(midia1)
play1.adicionarMidia(midia2)
play1.adicionarMidia(midia3)

play1.abrirPlaylist()
