# core/models/playlist.py

# Importa o módulo models do Django para herança
from django.db import models
from datetime import datetime
from .midia import Midia # Importa o Model Midia para relacionamento

class Playlist(models.Model): 
    idPlaylist = models.AutoField(db_column='id_Playlist',primary_key=True)
    nomePlaylist = models.CharField(db_column='Nome_Playlist', max_length=255, blank=True, null=True, unique=True, verbose_name="Título da Playlist")
    #ativa = models.BooleanField(default=False, verbose_name="Playlist Ativa")
    
    def cadastrarPlaylistORM(self):
        if not self.nomePlaylist:
            raise ValueError("Nome da playlist é obrigatório para cadastrar")
        
        try:
            play, created = Playlist.objects.get_or_create(
                nomePlaylist = self.nomePlaylist,
            )

            if not created:
                play.nomePlaylist = self.nomePlaylist
                play.save()

            self.idPlaylist = play.idPlaylist
            return self.idPlaylist
        
        except Exception as e:
            print("Erro ao cadastrar ou atualizar playlist: ", str(e))    
            raise

    class Meta:
        db_table = 'playlist'
        managed = False    


    def __str__(self):
        return self.nomePlaylist
        

#class ItemPlaylist(models.Model):
#    playlist = models.ForeignKey(
#        Playlist, 
#        related_name='itens', 
#        on_delete=models.CASCADE
#    )
#    midia = models.ForeignKey(
#        Midia, 
#        on_delete=models.CASCADE
#    )
#    ordem = models.PositiveIntegerField(verbose_name="Ordem de Exibição") 
    
#    class Meta:
#        ordering = ['ordem']
#        unique_together = ('playlist', 'ordem') 
        
#    def __str__(self):
#        return f"{self.playlist.titulo} - {self.midia.titulo} ({self.ordem})"
