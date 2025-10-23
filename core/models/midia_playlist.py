from .midia import Midia
from .playlist import Playlist
from django.db import models

class Midia_Playlist(models.Model):
    
    id_MP = models.AutoField(db_column='Id_MidiaPlaylist', primary_key=True)
    id_midia = models.ForeignKey(Midia, on_delete=models.CASCADE, db_column='Id_Midia')
    id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, db_column='Id_Playlist', related_name='itens',)
    ordem_midia = models.IntegerField(db_column='Ordem_Midia', default=0, verbose_name="Ordem de Exibição")

    def associarMP(self):
        try:
                midiaPlaylist, created = Midia_Playlist.objects.get_or_create(
                    id_midia=self.id_midia,
                    id_playlist=self.id_playlist,
                    defaults={
                        'ordem_midia': self.ordem_midia,
                    }
                )

                if not created:
                    midiaPlaylist.ordem_midia = self.ordem_midia
                    midiaPlaylist.save()

                self.id_MP = midiaPlaylist.id_MP
                return self.id_MP
            
        except Exception as e:
            print('Erro ao cadastrar ou atualizar uma associacao entre midia e playlist: ', str(e))
            raise 
                    

    class Meta:
       db_table = 'midia_playlist'
       managed = False
       unique_together = (('id_midia', 'id_playlist'), ('id_playlist', 'ordem_midia'))
       ordering = ['ordem_midia']

    def __str__(self):
        return f"{self.id_playlist.nomePlaylist} - {self.id_midia.titulo} ({self.ordem_midia})"   

