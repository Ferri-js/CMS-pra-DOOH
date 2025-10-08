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
# ----------------------------------------------------

class Midia(models.Model): # Esta classe é o que o Admin e o Django esperam
    # Campos baseados no MidiaDB, mas adaptados para o Django:
    titulo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50) # O tipo deve ser uma string (ex: 'video', 'imagem')
    url = models.URLField(max_length=500) # URLField é melhor para links
    data_upload = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='ativo')
    duracao = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Mídias"
        
    def __str__(self):
        return self.titulo