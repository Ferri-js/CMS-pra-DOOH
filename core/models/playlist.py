# core/models/playlist.py

# Importa o módulo models do Django para herança
from django.db import models
from .midia import Midia # Importa o Model Midia para relacionamento

# --- MODELS DO DJANGO (Versão Limpa e Funcional) ---
# Esta é a versão que o Admin, Migrações e Views usarão.

class Playlist(models.Model): 
    # Mantenha seus campos limpos. O código do seu colega tinha campos diferentes.
    titulo = models.CharField(max_length=100, unique=True, verbose_name="Título da Playlist")
    ativa = models.BooleanField(default=False, verbose_name="Playlist Ativa")
    
    def __str__(self):
        return self.titulo
        
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

# -------------------------------------------------------------------------
# --- CÓDIGO LEGADO SQL DO SEU COLEGA (MANTIDO APENAS PARA REFERÊNCIA) ---
# -------------------------------------------------------------------------
"""
# NOTA: O código abaixo foi comentado para evitar conflitos de sintaxe com o Django ORM.
# Ele serve como referência para a lógica de inserção direta no MySQL.

# Originalmente, o seu colega tinha esta classe:
# class Playlist(models.Model): # Ele usou models.Model, mas a lógica era SQL
#    idPlaylist = models.AutoField(db_column='Id_Playlist', primary_key=True)
#    nomePlaylist = models.CharField(db_column='Nome_Playlist', max_length=255, blank=True, null=True)

#    def cadastrarPlaylistORM(self):
#        # ... lógica de get_or_create e save ORM ...

#    class Meta:
#        db_table = 'playlist'
#        managed = False # Indica que esta tabela é gerenciada externamente (não pelo Django)
        
# Código Complexo de SQL Direto (MANTIDO SOMENTE AQUI DENTRO DO COMENTÁRIO)
# def cadastrarPlaylist(self):
#     # ... código longo de conexão e execução de comandos INSERT INTO ...
#     pass
"""