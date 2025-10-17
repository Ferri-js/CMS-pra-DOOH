import mysql.connector as mysql_connector
from mysql.connector import errorcode
from .tipoDispositivo import TipoDispositivo  # Enum esperado
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

    """ def __init__(self, idDispositivo, nomeDispositivo, tipoDispositivo, armazenamento, status, comprimento, largura, cod_verificacao):
        self.idDispositivo = idDispositivo
        self.nomeDispositivo = nomeDispositivo
        self.tipoDispositivo = tipoDispositivo
        self.armazenamento = armazenamento
        self.status = status
        self.comprimento = comprimento
        self.largura = largura
        self.cod_verificacao = cod_verificacao
        self.playlistAssociada = []"""

    def reproduzirPlaylist(self):
        pass

    """def cadastrarDispositivo(self):
        conexao, cursor = conectarBancoDados()

        try:
            conexao.start_transaction()
            verificarTabela(conexao, cursor)
            
            if not self.nomeDispositivo:
                raise TypeError("Nome é obrigatório para cadastrar o dispositivo.")
            
            tipoDispId = verificarTipo(self.tipoDispositivo)
            if tipoDispId == 0:
                raise TypeError("Tipo de dispositivo não identificado.")

            row = verificarIdExistente(self.idDispositivo, cursor)

            if not row:
                self.tipoDispositivo = tipoDispId  # substitui enum por int
                idDisp = self.insertTabela(conexao, cursor)
            else:
                idDisp = 0  # já existe

            return idDisp

        except mysql_connector.Error as err:
            conexao.rollback()
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise RuntimeError("Usuário/senha do MySQL inválidos.") from err
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise RuntimeError("Banco de dados não existe.") from err
            else:
                raise
        finally:
            cursor.close()
            conexao.close()    """



    


def conectarBancoDados():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "db",
    }

    conn = mysql_connector.connect(**db_config)
    cur = conn.cursor()
    return conn, cur

def verificarTabela(conn, cur):
    #conn.start_transaction()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS dispositivo (
            Id_Dispositivo INT AUTO_INCREMENT PRIMARY KEY,
            Tipo_Dispositivo_ID INT NOT NULL,
            Nome VARCHAR(255),
            Codigo_Vericacao VARCHAR(255),
            Comprimento INT NOT NULL,
            Largura INT NOT NULL,
            Armazenamento INT NOT NULL,
            Status VARCHAR(255),
            Uptime DATETIME
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

def verificarTipo(tipo):
    if isinstance(tipo, TipoDispositivo):
        return tipo.value
    elif isinstance(tipo, int):
        return tipo
    else:
        return 0

def verificarIdExistente(id, cur):
    cur.execute("SELECT Id_Dispositivo FROM dispositivo WHERE Id_Dispositivo = %s", (id,))
    return cur.fetchone()
