from .dispositivo import Dispositivo
from .playlist import Playlist
from django.db import models

class Dispositivo_Playlist(models.Model):
    
    id = models.AutoField(db_column='Id_DispPlaylist', primary_key=True)
    id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, db_column='Id_Playlist')
    id_dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, db_column='Id_Dispositivo')
    ordem_playlist = models.IntegerField(db_column='Ordem_Playlist', default=0)

    def associarDispPlay(self):
        try:
            dispPlaylist, created = Dispositivo_Playlist.objects.get_or_create(
                id_playlist=self.id_playlist,
                id_dispositivo=self.id_dispositivo,
                defaults={
                    'ordem_playlist': self.ordem_playlist,
                }
            )

            if not created:
                dispPlaylist.ordem_playlist = self.ordem_playlist
                dispPlaylist.save()

            self.id = dispPlaylist.id    
            return self.id
            
        except Exception as e:
            print('Erro ao cadastrar ou atualizar uma associacao entre dispositivo e playlist: ', str(e))
            raise

    class Meta:
        db_table = 'dispositivo_playlist'
        managed = False
        unique_together = (('id_playlist', 'id_dispositivo'),)    
        
    
