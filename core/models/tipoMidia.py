from django.db import models 

class tipoFormato(models.Model):
    id = models.AutoField(db_column='Id_Tipo_Midia', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=255)

    class Meta:
        db_table = 'tipos_midia'
        managed = False  # se a tabela já existe no banco e você não quer que o Django a modifique  

    def __str__(self):
        return self.nome      