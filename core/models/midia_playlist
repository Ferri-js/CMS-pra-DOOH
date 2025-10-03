import mysql.connector as mysql_connector
from mysql.connector import errorcode

class Midia_Playlist:
    
    def __init__(self, idMidiaPlaylist, idMidia, idPlaylist, ordem):
        self.idMidiaPlaylist = idMidiaPlaylist
        self.idMidia = idMidia
        self.idPlaylist = idPlaylist
        self.ordemMidia = ordem

    def associar(self):
        conexao, cursor = conectarBancoDados()
        try:
            conexao.start_transaction()
            verificarTabela(conexao, cursor)

            if not self.idMidia:
                raise TypeError("idMidia é obrigatório para cadastrar o dispositivo.")
            
            if not self.idPlaylist:
                raise TypeError("idPlaylist é obrigatório para cadastrar o dispositivo.")
            
    
            row = verificarIdExistente(self.idMidia, cursor)

            if not row:
                idMidiaPlaylist = self.insertTabela(conexao, cursor)
            else:
                idMidiaPlaylist = 0  # já existe

            return idMidiaPlaylist

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
            INSERT INTO midia_playlist (
                Id_MidiaPlaylist, Id_Midia, Id_Playlist, Ordem_Midia,
            )
            VALUES (%s,, %s, %s, %s)
            """,
            (
                self.idMidiaPlaylist,
                self.idMidia,
                self.idPlaylist,
                self.ordemMidia,
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
            Id_MidiaPlaylist INT AUTO_INCREMENT PRIMARY KEY,
            Id_Midia INT NOT NULL,
            Id_Playlist INT NOT NULL,
            Ordem_Midia INT NOT NULL,
            FOREIGN KEY (Id_Midia) REFERENCES dispositivo(Id_Dispositivo),
            FOREIGN KEY (Id_Playlist) REFERENCES playlist(Id_Playlist)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )    


def verificarIdExistente(id, cur):
    cur.execute("SELECT Id_MidiaPlaylist FROM dispositivo WHERE Id_MidiaPlaylist = %s", (id,))
    return cur.fetchone()    