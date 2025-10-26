# core/models/midia.py

# Imports do Django
from django.db import models
from django.core.files.storage import default_storage 
from django.conf import settings
# Imports de Cloud (Mantenha esses imports, mas a lógica real está na função)
from pathlib import Path
from pcloud import PyCloud 
import requests 
from datetime import datetime

# --- CONFIGURAÇÃO DE CHOICES (Tipo Selecionável) ---
MIDIA_CHOICES = [
    ('VIDEO', 'Vídeo (MP4, MOV)'),
    ('IMAGEM', 'Imagem (JPG, PNG)'),
    ('HTML', 'HTML/Web (Anúncio Externo)'),
]
# ---------------------------------------------------


# --- MODEL DJANGO (Versão Limpa, Final e Completa) ---
class Midia(models.Model): 
    titulo = models.CharField(max_length=255, verbose_name="Título da Mídia")
    
    # 1. CAMPO TIPO: Agora é um menu SELECIONÁVEL no formulário
    tipo = models.CharField(
        max_length=10, 
        choices=MIDIA_CHOICES, # Usa a lista definida acima
        default='VIDEO',
        verbose_name="Tipo de Mídia"
    ) 
    
    # 2. CAMPO PARA RECEBER O UPLOAD
    arquivo_upload = models.FileField(
        upload_to='temp_uploads/',
        verbose_name="Arquivo de Upload",
        null=True,  
        blank=True  
    ) 
    
    # 3. CAMPO PARA ARMAZENAR O URL PÚBLICO (Resultado final)
    url_publica = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        verbose_name="URL de Exibição (Cloud)"
    ) 
    
    data_upload = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='ativo')
    duracao = models.IntegerField(null=True, blank=True, verbose_name="Duração (Segundos)")
    
    class Meta:
        verbose_name_plural = "Mídias"
        
    def __str__(self):
        return self.titulo

# --- LÓGICA DO CLOUD (FUNÇÃO QUE A VIEW CHAMA - Versão Adaptada) ---

# OBS: Esta função precisa ser chamada na View (views.py)
def cadastrarmidiaPcloud(arquivo_django, tipo_midia):
    pc = PyCloud(username='email@gmail.com', password='senha') 

    if not getattr(pc, "auth_token", None):
        print("❌ Falha na autenticação. Configure PyCloud.")
        return None 

    try:
        # AQUI VOCÊ CONECTARIA A LÓGICA DO SEU TIME PARA O UPLOAD REAL
        
        # SIMULAÇÃO: 
        fileid = 'GZzT2025' # ID fictício
        file_name = arquivo_django.name
        
        # MOCK DO RETORNO: Retorna o URL público gerado
        public_url = f"https://u.pcloud.link/{fileid}/{file_name}"
        print(f"--- [SIMULAÇÃO] URL GERADO PARA O CLOUD: {public_url} ---")
        return public_url

    except Exception as e:
        print(f"Erro na lógica de Cloud: {e}")
        return None
        

# --- CÓDIGO LEGADO DO SEU COLEGA ---
# ⚠️ Se você tem mais classes ou lógica legada neste arquivo, isole-a com """..."""
"""
# Exemplo de código legado que você pode isolar:
class MidiaDB:
    # ... código de conexão MySQL ...
    pass
"""