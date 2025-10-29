from django.db import models

class TipoDispositivo(models.Model):

    id = models.AutoField(db_column="Id_Tipo_Dispositivo", primary_key=True)
    nome = models.CharField(db_column="Nome", max_length=255)

    class Meta:
        db_table = 'tipos_dispositivo'
        managed = False

    def __str__(self):
        return self.nome         

