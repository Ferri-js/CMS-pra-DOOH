# core/models/midia.py
# (Mantenha todos os imports existentes do seu colega no topo)
import webbrowser
import mysql.connector as mysql_connector
from mysql.connector import errorcode
from datetime import datetime

from django.db import models # NOVO: Importe o módulo models do Django

class MidiaDB: # Antiga classe 'Midia', renomeada para evitar conflito
    def __init__(self, id, titulo, tipo, URL, dataUpload, status, duracao):
        self.id = id
        self.titulo = titulo
        self.tipo = tipo
        self.URL = URL
        self.dataUpload = dataUpload
        self.status = status
        self.duracao = duracao

    # Mantenha todos os métodos cadastrarMidia, exibirMidia e removerMidia aqui
    # ... código longo de cadastrarMidia...
    # ... código de exibirMidia...
    # ... código de removerMidia...
    
# ----------------------------------------------------
# 2. MODEL DO DJANGO (Para Admin, Migrações e ORM)
# core/models/midia.py

from django.db import models
from django.core.files.storage import default_storage 
# ... (Mantenha o código legado/MidiaDB do seu colega intacto ou comentado) ...


class Midia(models.Model): 
    # ⬇️ NOVO CAMPO 1: Recebe o upload (Tornamos opcional para o banco de dados)
    arquivo_upload = models.FileField(
        upload_to='temp_uploads/',
        verbose_name="Arquivo de Upload",
        null=True,  # Permite NULL no banco de dados
        blank=True  # Permite que o campo fique vazio no formulário
    ) 
    
    # ⬇️ NOVO CAMPO 2: URL Pública (Tornamos opcional para o banco de dados)
    url_publica = models.URLField(
        max_length=500, 
        null=True, # Permite NULL no banco de dados
        blank=True, # Permite que o campo fique vazio no formulário/admin
        verbose_name="URL de Exibição (Cloud)"
    ) 
    
    titulo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50) 
    
    # ⬇️ NOVO CAMPO 1: RECEBE O ARQUIVO NO UPLOAD DO FORMULÁRIO (Substitui o campo 'url' antigo)
    arquivo_upload = models.FileField(
        upload_to='temp_uploads/', 
        verbose_name="Arquivo de Upload"
    ) 
    
    # ⬇️ NOVO CAMPO 2: ARMAZENA O URL PÚBLICO GERADO PELO CLOUD
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