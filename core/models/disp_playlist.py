import mysql.connector as mysql_connector
from mysql.connector import errorcode

class Dispositivo_Playlist:
    
    def __init__(self, idDispPlaylist, idDispositivo, idPlaylist, ordem):
        self.idDispPlaylist = idDispPlaylist
        self.idDispositivo = idDispositivo
        self.idPlaylist = idPlaylist
        self.ordemPlaylist = ordem

    def associar(self):
        conexao, cursor = conectarBancoDados()
        try:
            conexao.start_transaction()
            verificarTabela(conexao, cursor)

            if not self.idDispositivo:
                raise TypeError("idDispositivo é obrigatório para cadastrar o dispositivo.")
            
            if not self.idPlaylist:
                raise TypeError("idPlaylist é obrigatório para cadastrar o dispositivo.")
            
    
            row = verificarIdExistente(self.idDispositivo, cursor)

            if not row:
                idDispPlaylist = self.insertTabela(conexao, cursor)
            else:
                idDispPlaylist = 0  # já existe

            return idDispPlaylist

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
            INSERT INTO dispositivo_playlist (
                Id_DispPlaylist, Id_Playlist, Id_Dispositivo, Ordem_Playlist,
            )
            VALUES (%s,, %s, %s, %s)
            """,
            (
                self.idDisPlaylist,
                self.idPlaylist,
                self.idDispositivo,
                self.ordemPlaylist,
            )
        )
        conn.commit()
        return cur.lastrowid        
      


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
        CREATE TABLE IF NOT EXISTS dispositivo_playlist (
            Id_DispPlaylist INT AUTO_INCREMENT PRIMARY KEY,
            Id_Playlist INT NOT NULL,
            Id_Dispositivo INT NOT NULL,
            Ordem_Playlist INT NOT NULL,
            FOREIGN KEY (Id_Dispositivo) REFERENCES dispositivo(Id_Dispositivo),
            FOREIGN KEY (Id_Playlist) REFERENCES playlist(Id_Playlist)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )    


def verificarIdExistente(id, cur):
    cur.execute("SELECT Id_DispPlaylist FROM dispositivo WHERE Id_DispPlaylist = %s", (id,))
    return cur.fetchone()    