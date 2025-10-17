# core/models/midia.py

# Imports do Django
from django.db import models
from django.core.files.storage import default_storage 
from django.conf import settings
from .tipoMidia import tipoFormato # Assumindo que esta classe existe
# Imports da Lógica do Cloud
from pathlib import Path
from pcloud import PyCloud # Assumindo que você instalou: pip install pcloud
import requests # Assumindo que você instalou: pip install requests
from datetime import datetime

# --- MODEL DJANGO (Versão Limpa) ---
class Midia(models.Model): 
    # Mantenha a versão limpa do seu Model
    titulo = models.CharField(max_length=255, verbose_name="Título da Mídia")
    tipo = models.CharField(max_length=50, verbose_name="Tipo de Mídia") 
    
    # 1. Campo para receber o arquivo do upload (FileField)
    arquivo_upload = models.FileField(
        upload_to='temp_uploads/',
        verbose_name="Arquivo de Upload",
        null=True,  
        blank=True  
    ) 
    
    # 2. Campo para armazenar o URL público (o resultado do upload do Cloud)
    url_publica = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        verbose_name="URL de Exibição (Cloud)"
    ) 
    
    data_upload = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='ativo')
    duracao = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Mídias"
        
    def __str__(self):
        return self.titulo

# --- LÓGICA DO CLOUD (FUNÇÃO DO SEU COLEGA) ---

# Você deve mudar a assinatura desta função para receber o 'arquivo_django' e o 'tipo_midia'
# E retornar apenas o URL, para ser usada pela View.
def cadastrarmidiaPcloud(arquivo_django): # Removi os parâmetros originais
    pc = PyCloud(username='email@gmail.com', password='senha') 

    if not getattr(pc, "auth_token", None):
        print("❌ Falha na autenticação.")
        return None # Retorna None em caso de falha

    # SALVA O ARQUIVO LOCALMENTE (Temporário)
    try:
        # PCloud precisa do arquivo no disco. Seus colegas provavelmente salvam no MEDIA_ROOT primeiro.
        # Isto é uma SIMULAÇÃO do que a View fará:
        path_temp = Path(settings.MEDIA_ROOT) / 'temp_uploads' / arquivo_django.name
        # O código do seu colega usava um caminho fixo:
        file_path = Path('C:/Users/danie/Desktop/Django_MediaPlayer/media_player/staticfiles/player/media/img2.jpg') 
        
        # Como o seu código Django já move o arquivo temporariamente, vamos usar um mock:
        upload_response = {'metadata': [{'fileid': '123456', 'name': arquivo_django.name}]} # Mock da resposta
        
    except Exception as e:
        print(f"Erro ao simular o upload: {e}")
        return None
        
    # --- logica feita por daniel e mackie ---
    if 'metadata' in upload_response and upload_response['metadata']:
        file_metadata = upload_response['metadata'][0]
        fileid = file_metadata['fileid']

        auth_token = pc.auth_token # Precisa ser o token autenticado
        url = 'https://api.pcloud.com/getfilepublink'
        
        # ... (O restante do código que gera o link) ...
        # Se funcionar, deve retornar a public_url

        # MOCK DO RETORNO:
        return f"https://u.pcloud.link/{fileid}/{file_metadata['name']}"

    return None

# # REMOÇÃO DO CÓDIGO LEGADO NÃO DJANGO PARA EVITAR CONFLITO
# class Midia(models.Model): ... # <--- REMOVIDO!
# def cadastrarMidia(self): ... # <--- REMOVIDO!
# def exibirMidia(self): ... # <--- REMOVIDO!
# def removerMidia(self): ... # <--- REMOVIDO!