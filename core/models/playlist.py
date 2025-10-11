# core/models/playlist.py

from django.db import models
from .midia import Midia # Importa seu Model Midia

# Model de Playlist (Agrupador)
class Playlist(models.Model): 
    titulo = models.CharField(max_length=100, unique=True, verbose_name="Título da Playlist")
    ativa = models.BooleanField(default=False, verbose_name="Playlist Ativa")
    
    def __str__(self):
        return self.titulo
        
# Model de Item da Playlist (Ordem)
class ItemPlaylist(models.Model):
    playlist = models.ForeignKey(
        Playlist, 
        related_name='itens', 
        on_delete=models.CASCADE
    )
    midia = models.ForeignKey(
        Midia, 
        on_delete=models.CASCADE
    )
    ordem = models.PositiveIntegerField(verbose_name="Ordem de Exibição") 
    
    class Meta:
        ordering = ['ordem']
        unique_together = ('playlist', 'ordem') 
        
    def __str__(self):
        return f"{self.playlist.titulo} - {self.midia.titulo} ({self.ordem})"