from .tipoDispositivo import TipoDispositivo  
#from disp_playlist import Dispositivo_Playlist
from django.db import models 
from django.db import transaction
class Dispositivo(models.Model):

    idDispositivo = models.AutoField(db_column="Id_Dispositivo", primary_key=True)
    tipoDispositivo = models.ForeignKey(TipoDispositivo, on_delete=models.CASCADE, db_column='Tipo_Dispositivo_Id')
    nomeDispositivo = models.CharField(db_column='Nome', max_length=255)
    codVerificacao = models.CharField(db_column='Codigo_Verificacao', max_length=255, unique=True)
    status = models.IntegerField(db_column='Status', null=True, blank=True)
    #playlistAssociada = models.ManyToManyField(Playlist)

    def cadastrarDispositivoORM(self):
        if not self.nomeDispositivo:
            raise ValueError('Nome é obrigatório para cadastrar Dispositivo')
        
        if isinstance(self.tipoDispositivo, TipoDispositivo):
            tipoDispId = self.tipoDispositivo.id
        elif isinstance(self.tipoDispositivo, int):
            tipoDispId = self.tipoDispositivo
        else:
            raise ValueError('Tipo de dispositivo nao reconhecido')      

        try:
            dispositivo, created = Dispositivo.objects.get_or_create(
                nomeDispositivo = self.nomeDispositivo,
                defaults={
                    'tipoDispositivo':self.tipoDispositivo,
                    'status':self.status,
                    'codVerificacao':self.codVerificacao,
                }
            )
                 
            if not created:
                dispositivo.nomeDispositivo = self.nomeDispositivo
                dispositivo.status = self.status
                dispositivo.codVerificacao = self.codVerificacao
                dispositivo.tipoDispositivo_id = tipoDispId
                dispositivo.save()
                
            self.idDispositivo = dispositivo.idDispositivo
            return self.idDispositivo
              
    
        except Exception as e:
            print('Erro ao cadastrar ou atualizar Dispositivo: ', str(e))
            raise

    class Meta:
        db_table = 'dispositivo'
        managed = False
        verbose_name_plural = "Dispostivos"

