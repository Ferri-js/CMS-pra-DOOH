import webbrowser
from .tipoMidia import tipoFormato
import mysql.connector as mysql_connector
from mysql.connector import errorcode
from datetime import datetime
from pathlib import Path
from pcloud import PyCloud
import requests
from django.db import models 
from django.db import transaction
from datetime import datetime
#from midia_playlist import Midia_Playlist


class Midia(models.Model):
    id = models.AutoField(db_column='Id_Midia', primary_key=True)
    titulo = models.CharField(db_column = 'Titulo', max_length=255, null=True, blank=True)
    tamanho = models.IntegerField(db_column='Tamanho', null=True)
    tipo_midia = models.ForeignKey(tipoFormato, on_delete=models.CASCADE,db_column='Tipo_Midia_Id')
    url = models.CharField(db_column='URL', max_length=255, unique=True)
    status = models.IntegerField(db_column='Status', null=True, blank=True)
    duracao = models.IntegerField(db_column='Duracao', null=True, blank=True)
    data_upload = models.DateTimeField(db_column='Data_Upload', null=True)



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
        
      
     # None

    class Meta:
        db_table = 'midia'
        managed = False  # se a tabela já existe no banco e você não quer que o Django a modifique  

    def exibirMidia(self):
        print(f"ID: {self.id}, Título: {self.titulo}, Tipo: {self.tipo}")
        if self.URL:
            webbrowser.open(self.URL)

    def removerMidia(self):
        if not self.id:
            raise ValueError("ID da mídia não definido.")

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "database": "db",
        }

        conn = mysql_connector.connect(**db_config)
        cur = conn.cursor()
        try:
            conn.start_transaction()
            cur.execute("DELETE FROM Midia WHERE Id_Midia = %s", (self.id,))
            conn.commit()
            print(f"Mídia com ID {self.id} removida com sucesso.")
            self.id = None
        except mysql_connector.Error as err:
            conn.rollback()
            print(f"Erro ao remover mídia: {err}")
            raise
        finally:
            try:
                cur.close()
            except Exception:
                pass
            conn.close()

    def cadastrarMidiaPcloud():
        pc = PyCloud(username='email@gmail.com', password='senha') 

        if not getattr(pc, "auth_token", None):
            print("❌ Falha na autenticação.")
            return

        file_path = Path('C:/Users/danie/Desktop/Django_MediaPlayer/media_player/staticfiles/player/media/img2.jpg')

        upload_response = pc.uploadfile(files=[str(file_path)], folderid=0)

        if 'metadata' in upload_response and upload_response['metadata']:
            file_metadata = upload_response['metadata'][0]
            fileid = file_metadata['fileid']

            auth_token = pc.auth_token
            url = 'https://api.pcloud.com/getfilepublink'
            params = {
                'auth': auth_token,
                'fileid': fileid
            }

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # Garante que status != 200 levanta erro

                try:
                    publish_response = response.json()
                except ValueError:
                    print("❌ Resposta não está em JSON:", response.text)
                    return

                if publish_response.get('result') == 0:
                    public_url = publish_response.get('link')
                    print("✅ Upload realizado com sucesso!")
                    print("Arquivo:", file_metadata.get('name'))
                    print("Link público:", public_url)
                else:
                    print("❌ Erro ao gerar link público.")
                    print("Resposta:", publish_response)

            except requests.exceptions.RequestException as e:
                print(f"❌ Erro na requisição: {e}")
                print("Resposta:", response.text if response else "Nenhuma resposta")
        else:
            print("❌ Erro ao fazer upload.")
            print("Resposta:", upload_response)

            