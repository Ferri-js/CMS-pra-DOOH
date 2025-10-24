import uuid
import webbrowser
from .tipoMidia import tipoFormato
from datetime import datetime
from pathlib import Path
#from pcloud import PyCloud
import requests
from django.db import models 
from django.db import transaction
from django.core.files.storage import default_storage
from django.conf import settings 
from datetime import datetime
from supabase import create_client
#from midia_playlist import Midia_Playlist
import os
import mimetypes


class Midia(models.Model):
    id = models.AutoField(db_column='Id_Midia', primary_key=True)
    titulo = models.CharField(db_column = 'Titulo', max_length=255, null=True, blank=True, verbose_name="Título da Mídia")
    tamanho = models.IntegerField(db_column='Tamanho', null=True)
    tipo_midia = models.ForeignKey(tipoFormato, on_delete=models.CASCADE,db_column='Tipo_Midia_Id', verbose_name="Tipo de Mídia", null=True)
    url = models.CharField(db_column='URL', max_length=255, unique=True, verbose_name="URL de Exibição")
    status = models.IntegerField(db_column='Status', null=True, blank=True, default=1)
    duracao = models.IntegerField(db_column='Duracao', null=True, blank=True)
    data_upload = models.DateTimeField(db_column='Data_Upload', null=True, auto_now_add=True)


     # 1. Campo para receber o arquivo do upload (FileField)
    arquivo_upload = models.FileField(
        #upload_to='temp_uploads/',
        db_column='caminho_midia',    
        verbose_name="Arquivo de Upload",
        null=True,  
        blank=True  
    ) 
    
    def cadastrarMidia(self):  
      if not self.url:
            raise ValueError('URL obrigatório para cadastrar mídia')
      
        # Determina tipo_id com segurança
      if isinstance(self.tipo_midia, tipoFormato):
            tipo_id = self.tipo_midia.id  # ou .value se for enum — mas aqui é um model
      elif isinstance(self.tipo_midia, int):
            tipo_id = self.tipo_midia
      else:
           raise TypeError("Tipo de mídia deve ser um tipoFormato ou um inteiro correspondente ao ID.")

      try:
                try:
                    midia, created = Midia.objects.get_or_create(
                        url=self.url,
                        defaults={
                            'titulo': self.titulo,
                            'tipo_midia': self.tipo_midia,
                            'status': self.status,
                            'duracao': self.duracao,
                            'data_upload': self.data_upload,
                        }
                    )
                except Exception as e:
                    print("Erro ao cadastrar midia:", e)
                    raise

                if not created:
                    # Atualiza os campos se já existir
                    midia.titulo = self.titulo
                    midia.tipo_midia_id = tipo_id
                    midia.status = self.status
                    midia.duracao = self.duracao
                    midia.data_upload = self.data_upload if isinstance(self.data_upload, datetime) else datetime.combine(self.data_upload, datetime.min.time())
                    midia.save()

                self.id = midia.id
                return midia.id
      except Exception as e:
            raise RuntimeError("Erro ao cadastrar ou atualizar mídia.") from e     
        
    class Meta:
        db_table = 'midia'
        managed = False  # se a tabela já existe no banco e você não quer que o Django a modifique  
        verbose_name_plural = "Mídias"

    def __str__(self):
        return self.titulo
    
    def cadastrarMidiaSupabase():
        nome_bucket = "NexxoMedias"
        pasta_bucket = "medias"
        SUPABASE_URL="https://tvrvftpiozxlubejbzmu.supabase.co"
        SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cnZmdHBpb3p4bHViZWpiem11Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA4NDk5NjgsImV4cCI6MjA3NjQyNTk2OH0.itPIuGqmk9QTpj9cJMeQqeIRIZpoKDH8AUIfvNsu1Qk"

        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        links = []
        dir = "C:/Users/danie/Desktop/Django_MediaPlayer/media_player/staticfiles/player/media/"
        midias = os.listdir(dir)

        for arquivo in midias:
            caminho_arq = os.path.join(dir, arquivo)
            if os.path.isfile(caminho_arq):
                with open(caminho_arq, "rb") as arq:  
                    dados = arq.read()

                #caminho_bucket_supabase = f"{arquivo}"
                nome_unico = f"{pasta_bucket}/{uuid.uuid4().hex}_{arquivo}"

                mime_type, _ = mimetypes.guess_type(caminho_arq)
                if not mime_type:
                    mime_type = "application/octet-stream"

                #Verifica erro
                try:
                    upload = supabase.storage.from_(nome_bucket).upload(nome_unico, dados, {"content-type": mime_type})
                except Exception as e:
                    print(f"Erro ao enviar {arquivo}: {e}")
                    continue   

                #Gera URL publica
                url = supabase.storage.from_(nome_bucket).get_public_url(nome_unico)
                links.append(url)
        print(links)
        return links               
     





