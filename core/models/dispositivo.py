import mysql.connector as mysql_connector
from mysql.connector import errorcode
from tipoDispositivo import TipoDispositivo  # Enum esperado
from disp_playlist import Dispositivo_Playlist

class Dispositivo:
    def __init__(self, idDispositivo, nomeDispositivo, tipoDispositivo, armazenamento, status, comprimento, largura, cod_verificacao):
        self.idDispositivo = idDispositivo
        self.nomeDispositivo = nomeDispositivo
        self.tipoDispositivo = tipoDispositivo
        self.armazenamento = armazenamento
        self.status = status
        self.comprimento = comprimento
        self.largura = largura
        self.cod_verificacao = cod_verificacao
        self.playlistAssociada = []

    def reproduzirPlaylist(self):
        pass

    def cadastrarDispositivo(self):
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
            conexao.close()

    def insertTabela(self, conn, cur):
        cur.execute(
            """
            INSERT INTO dispositivo (
                Tipo_Dispositivo_Id, Uptime, Status, Comprimento, Largura,
                Nome, Codigo_Vericacao, Armazenamento
            )
            VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s)
            """,
            (
                self.tipoDispositivo,
                self.status,
                self.comprimento,
                self.largura,
                self.nomeDispositivo,
                self.cod_verificacao,
                self.armazenamento,
            )
        )
        conn.commit()
        return cur.lastrowid
    
    def associarPlaylist(self, idPlaylist, ordem):
        associacao = Dispositivo_Playlist(
        idDispPlaylist = None,
        idDispositivo = self.idDispositivo,
        idPlaylist = idPlaylist,
        ordemPlaylist = ordem
    )
        
        associacao.associar()
        self.playlistAssociada.append(idPlaylist)



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
