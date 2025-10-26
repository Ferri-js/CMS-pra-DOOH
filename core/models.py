# core/models.py  <-- ARQUIVO ÚNICO PARA MODELS DJANGO

from django.db import models
from django.conf import settings # Pode ser útil para relacionamentos com User no futuro
import time # Para a função Cloud (simulação)
from pathlib import Path
# Se der erro aqui, instale com 'pip install pypcloud' ou 'pip install pcloud'
try:
    from pcloud import PyCloud 
except ImportError:
    PyCloud = None # Define como None se não estiver instalado, evita erro inicial
import requests # Se der erro, instale com 'pip install requests'
from datetime import datetime

# --- CONFIGURAÇÃO DE CHOICES (Tipo Selecionável) ---
MIDIA_CHOICES = [
    ('VIDEO', 'Vídeo (MP4, MOV)'),
    ('IMAGEM', 'Imagem (JPG, PNG)'),
    ('HTML', 'HTML/Web (Anúncio Externo)'),
]

# --- Model TipoDispositivo ---
class TipoDispositivo(models.Model):
    # O Django gerencia o ID automaticamente
    nome = models.CharField(max_length=255, verbose_name="Nome do Tipo")

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Tipo de Dispositivo"
        verbose_name_plural = 'Tipos de Dispositivo'

# --- Model Midia ---
class Midia(models.Model): 
    titulo = models.CharField(max_length=255, verbose_name="Título da Mídia")
    tipo = models.CharField(
        max_length=10, 
        choices=MIDIA_CHOICES, 
        default='VIDEO',
        verbose_name="Tipo de Mídia"
    ) 
    arquivo_upload = models.FileField(
        upload_to='temp_uploads/', # Diretório temporário dentro de MEDIA_ROOT
        verbose_name="Arquivo de Upload",
        null=True,  
        blank=True  
    ) 
    url_publica = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        verbose_name="URL de Exibição (Cloud)"
    ) 
    data_upload = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='ativo') # Usar CharField para status é mais flexível
    duracao = models.IntegerField(null=True, blank=True, verbose_name="Duração (Segundos)")
    
    class Meta:
        verbose_name = "Mídia"
        verbose_name_plural = "Mídias"
        
    def __str__(self):
        return self.titulo

# --- Model Playlist ---
class Playlist(models.Model):
    titulo = models.CharField(max_length=100, unique=True, verbose_name="Título da Playlist")
    ativa = models.BooleanField(default=False, verbose_name="Playlist Ativa?")
    
    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"

# --- Model ItemPlaylist ---
class ItemPlaylist(models.Model):
    playlist = models.ForeignKey(Playlist, related_name='itens', on_delete=models.CASCADE)
    midia = models.ForeignKey(Midia, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(verbose_name="Ordem de Exibição")
    
    class Meta:
        ordering = ['ordem'] # Garante a ordem padrão ao buscar
        unique_together = ('playlist', 'ordem') # Não permite mesma ordem na mesma playlist
        verbose_name = "Item da Playlist"
        verbose_name_plural = "Itens da Playlist"
        
    def __str__(self):
        # Tenta mostrar o título da mídia se o objeto midia estiver carregado
        midia_titulo = self.midia.titulo if hasattr(self.midia, 'titulo') else f"Mídia ID {self.midia_id}"
        playlist_titulo = self.playlist.titulo if hasattr(self.playlist, 'titulo') else f"Playlist ID {self.playlist_id}"
        return f"{playlist_titulo} - Item {self.ordem}: {midia_titulo}"

# --- Model Dispositivo ---
class Dispositivo(models.Model):
    nomeDispositivo = models.CharField(max_length=255, verbose_name="Nome do Dispositivo")
    codVerificacao = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Código de Verificação"
    )
    status = models.CharField(max_length=20, default='ativo', verbose_name="Status") # Ex: 'ativo', 'inativo', 'offline'
    
    # Relações limpas (ForeignKey)
    tipoDispositivo = models.ForeignKey(
        TipoDispositivo, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Tipo de Dispositivo"
    )
    playlistAssociada = models.ForeignKey(
        Playlist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Playlist Associada"
    )

    def __str__(self):
        return self.nomeDispositivo
    
    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = 'Dispositivos'


# --- LÓGICA DO CLOUD (PODE FICAR AQUI OU EM OUTRO ARQUIVO UTILS.PY) ---
# 🚨 LEMBRETE: SUBSTITUA ESTA FUNÇÃO PELA IMPLEMENTAÇÃO REAL DO SEU TIME!
def cadastrarmidiaPcloud(arquivo_django, tipo_midia):
    # Verificação básica se a biblioteca foi importada
    if PyCloud is None:
        print("❌ Biblioteca 'pcloud' não instalada. Execute 'pip install pcloud'.")
        return None
        
    # --- SIMULAÇÃO ---
    print(f"--- INICIANDO UPLOAD (SIMULADO) PARA CLOUD: {arquivo_django.name} ({tipo_midia}) ---")
    time.sleep(0.5) 
    # Use um ID de arquivo e nome únicos para o URL de teste
    file_id_mock = hash(arquivo_django.name + str(time.time())) # Gera um ID "único" simples
    safe_filename = arquivo_django.name.replace(' ', '_')
    url_gerada = f"https://u.pcloud.link/publink/show?code={file_id_mock}_{safe_filename}" # Exemplo de URL pCloud
    print(f"--- UPLOAD (SIMULADO) CONCLUÍDO. URL GERADO: {url_gerada} ---")
    return url_gerada