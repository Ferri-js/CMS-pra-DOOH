from midia import Midia
import webbrowser

from datetime import datetime

try:
    import mysql.connector as mysql_connector
    from mysql.connector import errorcode as MYSQL_ERRORCODE
except ImportError:
    mysql_connector = None
    MYSQL_ERRORCODE = None

class Playlist:
    def __init__(self, idPlaylist, nomePlaylist):
        self.idPlaylist = idPlaylist
        self.nomePlaylist = nomePlaylist
        self.listaMidias = []
    

    def adicionarMidia(self, mid):
        self.listaMidias.append(mid)

    def removerMidia(self):
        if self.listaMidias:
            self.listaMidias.pop()


    def abrirPlaylist(self):
        for mid in self.listaMidias:
            webbrowser.open(mid.URL)

#py -m pip install mysql-connector-python
def cadastrarPlaylist(self):
    if mysql_connector is None:
        raise RuntimeError(
            "O pacote mysql-connector-python não está instalado. Instale com: pip install mysql-connector-python"
        )

    db_config = {
        "host": "localhost",
        "user": "seu_usuario",
        "password": "sua_senha",
        "database": "seu_banco",
    }

    tabela_playlist = "playlists"
    tabela_midia = "midias"
    tabela_rel = "playlist_midias"

    conn = mysql_connector.connect(**db_config)
    cur = conn.cursor()
    try:
        conn.start_transaction()

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {tabela_playlist} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                criada_em DATETIME NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {tabela_midia} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                url TEXT NOT NULL,
                tipo VARCHAR(50) NOT NULL,
                UNIQUE KEY uq_midia_url (url(255))
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {tabela_rel} (
                playlist_id INT NOT NULL,
                midia_id INT NOT NULL,
                ordem INT NOT NULL,
                PRIMARY KEY (playlist_id, midia_id),
                CONSTRAINT fk_rel_playlist FOREIGN KEY (playlist_id)
                    REFERENCES {tabela_playlist}(id) ON DELETE CASCADE,
                CONSTRAINT fk_rel_midia FOREIGN KEY (midia_id)
                    REFERENCES {tabela_midia}(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        nome_playlist = getattr(self, "nome", None) or "Playlist sem nome"
        cur.execute(
            f"INSERT INTO {tabela_playlist} (nome, criada_em) VALUES (%s, %s)",
            (nome_playlist, datetime.now()),
        )
        playlist_id = cur.lastrowid

        midias = getattr(self, "midias", []) or []
        for idx, m in enumerate(midias, start=1):
            titulo = getattr(m, "titulo", None) or (m.get("titulo") if isinstance(m, dict) else None)
            url = getattr(m, "url", None) or (m.get("url") if isinstance(m, dict) else None)
            tipo = getattr(m, "tipo", None) or (m.get("tipo") if isinstance(m, dict) else None)

            if not (titulo and url and tipo):
                raise ValueError(f"Mídia inválida na posição {idx}: precisa de titulo, url e tipo.")

            cur.execute(f"SELECT id FROM {tabela_midia} WHERE url=%s", (url,))
            row = cur.fetchone()
            if row:
                midia_id = row[0]
                cur.execute(
                    f"UPDATE {tabela_midia} SET titulo=%s, tipo=%s WHERE id=%s",
                    (titulo, tipo, midia_id)
                )
            else:
                cur.execute(
                    f"INSERT INTO {tabela_midia} (titulo, url, tipo) VALUES (%s, %s, %s)",
                    (titulo, url, tipo)
                )
                midia_id = cur.lastrowid

            cur.execute(
                f"INSERT INTO {tabela_rel} (playlist_id, midia_id, ordem) "
                f"VALUES (%s, %s, %s) "
                f"ON DUPLICATE KEY UPDATE ordem=VALUES(ordem)",
                (playlist_id, midia_id, idx)
            )

        conn.commit()
        return playlist_id

    except mysql_connector.Error as err:
        conn.rollback()
        if MYSQL_ERRORCODE and err.errno == MYSQL_ERRORCODE.ER_ACCESS_DENIED_ERROR:
            raise RuntimeError("Usuário/senha do MySQL inválidos.") from err
        elif MYSQL_ERRORCODE and err.errno == MYSQL_ERRORCODE.ER_BAD_DB_ERROR:
            raise RuntimeError("Banco de dados não existe.") from err
        else:
            raise
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()




    

    


        

