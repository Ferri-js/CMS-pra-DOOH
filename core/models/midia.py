# core/models/midia.py

import uuid
import os
import mimetypes
import time # Usado na simulação (pode remover se usar o Supabase real)

from django.db import models
from django.conf import settings
from .tipoMidia import tipoFormato # Importa o Model TipoDispositivo (que você renomeou)

# Tenta importar as bibliotecas de Cloud. Se não existirem, define como None.
try:
    from supabase import create_client
except ImportError:
    create_client = None
    print("AVISO: Biblioteca 'supabase' não instalada. Rode: pip install supabase")

try:
    from pcloud import PyCloud
except ImportError:
    PyCloud = None
    print("AVISO: Biblioteca 'pcloud' não instalada. Rode: pip install pcloud")


# ----------------------------------------------------
# MODELO DJANGO (Esta é a versão que o Django usará)
# ----------------------------------------------------

# Define as opções de tipo de mídia (para o campo 'tipo')
MIDIA_CHOICES = [
    ('VIDEO', 'Vídeo (MP4, MOV)'),
    ('IMAGEM', 'Imagem (JPG, PNG)'),
    ('HTML', 'HTML/Web (Anúncio Externo)'),
]

class Midia(models.Model):
    # ID automático do Django (PK)
    id = models.AutoField(primary_key=True) 
    
    titulo = models.CharField(max_length=255, verbose_name="Título da Mídia", null=True, blank=True)
    
    # Campo 'tipo' usando as CHOICES que definimos acima
    tipo = models.CharField(
        max_length=10, 
        choices=MIDIA_CHOICES, 
        default='VIDEO',
        verbose_name="Tipo de Mídia"
    ) 
    
    # Campo para receber o arquivo do usuário no formulário /gerenciar/
    arquivo_upload = models.FileField(
        upload_to='temp_uploads/', 
        verbose_name="Arquivo de Upload",
        null=True,  
        blank=True  
    ) 
    
    # Campo que armazena o URL final gerado pelo Cloud
    url_publica = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        verbose_name="URL de Exibição (Cloud)"
    ) 
    
    # Campos que seu colega tinha (adaptados para o Django)
    tamanho = models.IntegerField(null=True, blank=True) # Tamanho do arquivo
    status = models.CharField(max_length=50, default='ativo', verbose_name="Status") 
    duracao = models.IntegerField(null=True, blank=True, verbose_name="Duração (Segundos)")
    data_upload = models.DateTimeField(auto_now_add=True) # Data automática na criação

    class Meta:
        verbose_name = "Mídia"
        verbose_name_plural = "Mídias"
        # NÃO use 'managed = False' se você quiser que o Django controle esta tabela (recomendado)
        # managed = False 
        
    def __str__(self):
        return self.titulo

# ----------------------------------------------------
# LÓGICA DE UPLOAD PARA O CLOUD (SUPABASE)
# ----------------------------------------------------
# Esta função será chamada pela sua View 'gerenciar_midia'

def cadastrarmidiaPcloud(arquivo_django, tipo_midia_nome):
    """
    Função adaptada da branch 'Bd_Integrado_ORM'.
    Recebe o arquivo (UploadedFile do Django) e o tipo (string).
    Faz o upload para o Supabase e retorna o URL público.
    """
    
    # 🚨 NOTA: A lógica original do seu colega lia arquivos de uma pasta FIXA no PC.
    # Esta versão adaptada lê o arquivo que o usuário enviou pelo formulário Django.
    
    if not create_client:
        print("❌ Biblioteca 'supabase' não encontrada. Upload cancelado.")
        return None

    # 🚨 ATENÇÃO: Substitua pelas suas credenciais reais!
    SUPABASE_URL = "https://tvrvftpiozxlubejbzmu.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cnZmdHBpb3p4bHViZWpiem11Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA4NDk5NjgsImV4cCI6MjA3NjQyNTk2OH0.itPIuGqmk9QTpj9cJMeQqeIRIZpoKDH8AUIfvNsu1Qk"
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"❌ Erro ao conectar no Supabase: {e}")
        return None

    nome_bucket = "NexxoMedias"
    pasta_bucket = "medias" # Pasta dentro do bucket
    
    # Gera um nome único para o arquivo
    nome_arquivo_original = arquivo_django.name
    nome_unico = f"{pasta_bucket}/{uuid.uuid4().hex}_{nome_arquivo_original}"
    
    # Pega o tipo MIME do arquivo (ex: 'image/jpeg')
    mime_type = mimetypes.guess_type(nome_arquivo_original)[0]
    if not mime_type:
        mime_type = "application/octet-stream"

    try:
        print(f"--- INICIANDO UPLOAD PARA SUPABASE: {nome_arquivo_original} ---")
        
        # Lê o conteúdo do arquivo enviado pelo Django
        dados_arquivo = arquivo_django.read()
        
        # Faz o upload para o Supabase
        upload_response = supabase.storage.from_(nome_bucket).upload(
            file=dados_arquivo,
            path=nome_unico,
            file_options={"content-type": mime_type, "cache-control": "3600", "upsert": "false"}
        )
        
        # Gera o URL público
        url_publica = supabase.storage.from_(nome_bucket).get_public_url(nome_unico)
        
        print(f"--- UPLOAD CONCLUÍDO. URL GERADO: {url_publica} ---")
        return url_publica

    except Exception as e:
        print(f"❌ Erro ao enviar {nome_arquivo_original} para o Supabase: {e}")
        return None