import mysql.connector as mysql_connector
from mysql.connector import errorcode
from tipoDispositivo import TipoDispositivo # Enum esperado
from disp_playlist import Dispositivo_Playlist
from django.db import models
from tipoDispositivo import TipoDispositivo

from django.db import models, transaction
from .tipoDispositivo import TipoDispositivo
from .playlist import Playlist

class Dispositivo(models.Model):
    id = models.AutoField(db_column='Id_Dispositivo', primary_key=True)
    tipo_dispositivo = models.ForeignKey(TipoDispositivo, on_delete=models.CASCADE, db_column='Tipo_Dispositivo_Id', null=True)
    nome = models.CharField(db_column='Nome', max_length=255, null=True, blank=True)
    codigo_verificacao = models.CharField(db_column='Codigo_Vericacao', max_length=255, null=True, blank=True)
    comprimento = models.IntegerField(db_column='Comprimento', null=True)
    largura = models.IntegerField(db_column='Largura', null=True)
    armazenamento = models.IntegerField(db_column='Armazenamento', null=True)
    status = models.CharField(db_column='Status', max_length=255, null=True, blank=True)
    uptime = models.DateTimeField(db_column='Uptime', null=True, blank=True)

    class Meta:
        db_table = 'dispositivo'
        managed = False

    def __str__(self):
        return f"Dispositivo(id={self.id}, nome={self.nome})"

    def cadastrarDispositivo(self):
        """Cadastra o dispositivo usando Django ORM.

        Regras baseadas na implementação original:
        - `nome` é obrigatório para cadastrar
        - se `id` já existir no banco retorna 0 (não cria)
        - aceita `tipo_dispositivo` como instância de `TipoDispositivo` ou inteiro id
        """
        if not self.nome:
            raise ValueError('Nome é obrigatório para cadastrar o dispositivo')

        # Determina tipo_id com segurança
        if isinstance(self.tipo_dispositivo, TipoDispositivo):
            tipo_id = getattr(self.tipo_dispositivo, 'id', None) or getattr(self.tipo_dispositivo, 'pk', None)
        elif isinstance(self.tipo_dispositivo, int):
            tipo_id = self.tipo_dispositivo
        else:
            tipo_id = None

        if tipo_id is None:
            raise TypeError('Tipo de dispositivo não identificado.')

        with transaction.atomic():
            if self.id and Dispositivo.objects.filter(id=self.id).exists():
                return 0

            # atribui o FK por id caso tenhamos um inteiro
            if isinstance(self.tipo_dispositivo, int):
                self.tipo_dispositivo_id = self.tipo_dispositivo

            self.save()
            return self.id

    def associarPlaylist(self, playlist_or_id, ordem=0):
        """Associa este dispositivo a uma playlist (cria entrada em dispositivo_playlist)."""
        from .disp_playlist import Dispositivo_Playlist

        if isinstance(playlist_or_id, Playlist):
            playlist = playlist_or_id
        else:
            playlist = Playlist.objects.get(pk=playlist_or_id)

        assoc, created = Dispositivo_Playlist.objects.get_or_create(
            dispositivo=self,
            playlist=playlist,
            defaults={'ordem_playlist': ordem}
        )
        return assoc.id if created else 0
