# core/models/midia.py
import uuid
import mimetypes
import os
import time
from pathlib import Path
from django.db import models
from django.conf import settings
from .tipoMidia import tipoFormato # Importa o Model TipoDispositivo

# Tenta importar as bibliotecas de Cloud
try:
    from supabase import create_client, Client
except ImportError:
    create_client = None
    print("AVISO: Biblioteca 'supabase' não instalada.")
try:
    from pcloud import PyCloud
except ImportError:
    PyCloud = None

# --- CONFIGURAÇÃO DE CHOICES (Tipo Selecionável) ---
MIDIA_CHOICES = [
    ('VIDEO', 'Vídeo (MP4, MOV)'),
    ('IMAGEM', 'Imagem (JPG, PNG)'),
    ('HTML', 'HTML/Web (Anúncio Externo)'),
]

# --- MODELO DJANGO (Esta é a única classe 'Midia' que o Django usará) ---
class Midia(models.Model):
    id = models.AutoField(db_column='Id_Midia', primary_key=True) 
    titulo = models.CharField(max_length=255, verbose_name="Título da Mídia", null=True, blank=True)
    
    tipo = models.CharField(
        max_length=10, 
        choices=MIDIA_CHOICES, 
        default='VIDEO',
        verbose_name="Tipo de Mídia"
    ) 
    
    arquivo_upload = models.FileField(
        upload_to='temp_uploads/', 
        verbose_name="Arquivo de Upload (Temporário)",
        null=True,  
        blank=True  
    ) 
    
    url_publica = models.URLField(
        db_column='URL', # Mapeia para a coluna 'URL' do banco legado
        max_length=500, 
        null=True, 
        blank=True, 
        verbose_name="URL de Exibição (Cloud)"
    ) 
    
    data_upload = models.DateTimeField(db_column='Data_Upload', auto_now_add=True, null=True, blank=True)
    status = models.CharField(db_column='Status', max_length=50, default='ativo')
    duracao = models.IntegerField(db_column='Duracao', null=True, blank=True)
    tamanho = models.IntegerField(db_column='Tamanho', null=True, blank=True) 
    
    class Meta:
        db_table = 'midia' 
        managed = False # Django não vai tentar criar ou alterar esta tabela
        verbose_name = "Mídia"
        verbose_name_plural = "Mídias"
        
    def __str__(self):
        return self.titulo

# --- LÓGICA DE UPLOAD PARA O CLOUD (SUPABASE) ---
def cadastrarmidiaPcloud(arquivo_django): 
    """
    Função adaptada da branch 'Bd_Integrado_ORM'.
    Recebe o arquivo (UploadedFile do Django).
    Faz o upload para o Supabase e retorna o URL público.
    """
    
    if not create_client:
        print("❌ Biblioteca 'supabase' não encontrada. Upload cancelado.")
        return None

    # 🚨 NOTA: O código original usava credenciais fixas (daniel.wteles@gmail.com)
    # E um caminho fixo (C:/Users/danie/Desktop...). 
    # A versão correta usa as variáveis de ambiente e o arquivo vindo do formulário.

    SUPABASE_URL = settings.SUPABASE_URL
    SUPABASE_KEY = settings.SUPABASE_KEY

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Credenciais SUPABASE_URL ou SUPABASE_KEY não definidas no settings.py")
        return None

    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"❌ Erro ao conectar no Supabase: {e}")
        return None

    nome_bucket = "NexxoMedias"
    pasta_bucket = "medias"
    
    nome_arquivo_original = arquivo_django.name
    nome_unico = f"{pasta_bucket}/{uuid.uuid4().hex}_{nome_arquivo_original}"
    
    mime_type, _ = mimetypes.guess_type(nome_arquivo_original)
    if not mime_type:
        mime_type = "application/octet-stream"

    try:
        print(f"--- INICIANDO UPLOAD PARA SUPABASE: {nome_arquivo_original} ---")
        
        dados_arquivo = arquivo_django.read()
        
        supabase.storage.from_(nome_bucket).upload(
            file=dados_arquivo,
            path=nome_unico,
            file_options={"content-type": mime_type, "cache-control": "3600", "upsert": "false"}
        )
        
        url_publica = supabase.storage.from_(nome_bucket).get_public_url(nome_unico)
        
        print(f"--- UPLOAD CONCLUÍDO. URL GERADO: {url_publica} ---")
        return url_publica

    except Exception as e:
        print(f"❌ Erro ao enviar {nome_arquivo_original} para o Supabase: {e}")
        return None