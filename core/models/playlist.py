import mysql.connector as mysql_connector
from mysql.connector import errorcode
from datetime import datetime
from midia_playlist import Midia_Playlist


class Playlist:
    def __init__(self, idPlaylist, nomePlaylist):
        self.idPlaylist = idPlaylist  # Se usar AUTO_INCREMENT, pode deixar None
        self.nomePlaylist = nomePlaylist
        self.listaMidias = []

    def adicionarMidia(self, mid):
        self.listaMidias.append(mid)

    def removerMidia(self):
        if self.listaMidias:
            self.listaMidias.pop()

    def cadastrarPlaylist(self):
        import mysql.connector as mysql_connector
        from mysql.connector import errorcode
        from datetime import datetime

    def associarPlaylist(self, idMidia, ordem):
        associacao = Midia_Playlist(
        idMidiaPlaylist = None,
        idPlaylist = self.idPlaylist,
        idMid = idMidia,
        ordemMidia = ordem
    )
        
        associacao.associar()
        self.listaMidias.append(idMidia)


        if mysql_connector is None:
            raise RuntimeError(
                "O pacote mysql-connector-python não está instalado. Instale com: pip install mysql-connector-python"
            )

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

            # Inserir na tabela Playlist (sem o ID, pois é AUTO_INCREMENT)
            cur.execute(
                "INSERT INTO Playlist (Nome_Playlist) VALUES (%s)",
                (self.nomePlaylist,)
            )
            playlist_id = cur.lastrowid

            # Inserir mídias e relacionamentos
            midias = getattr(self, "midias", []) or []

            for idx, m in enumerate(midias, start=1):
                titulo = getattr(m, "titulo", None) or (m.get("titulo") if isinstance(m, dict) else None)
                url = getattr(m, "URL", None) or (m.get("URL") if isinstance(m, dict) else None)
                tipo = getattr(m, "tipo", None) or (m.get("tipo") if isinstance(m, dict) else None)
                data_upload = getattr(m, "dataUpload", None)
                status = getattr(m, "status", None)
                duracao = getattr(m, "duracao", None)

                if not (titulo and url and tipo):
                    raise ValueError(f"Mídia inválida na posição {idx}: precisa de titulo, url e tipo.")

                # Verifica se a mídia já existe
                cur.execute("SELECT Id_Midia FROM Midia WHERE URL = %s", (url,))
                row = cur.fetchone()
                if row:
                    midia_id = row[0]
                    # Atualiza campos principais
                    cur.execute(
                        "UPDATE Midia SET Status = %s, Duracao = %s WHERE Id_Midia = %s",
                        (status, duracao, midia_id)
                    )
                else:
                    # Insere nova mídia
                    cur.execute(
                        """
                        INSERT INTO Midia (Tipo_Midia_Id, Status, Duracao, Data_Upload, URL)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (1, status, duracao, data_upload, url)
                    )
                    midia_id = cur.lastrowid

                # Relacionamento na tabela Midia_Playlist
                cur.execute(
                    """
                    INSERT INTO Midia_Playlist (Id_Midia, Id_Playlist, Ordem_Midia)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE Ordem_Midia = VALUES(Ordem_Midia)
                    """,
                    (midia_id, playlist_id, idx)
                )

            conn.commit()
            return playlist_id

        except mysql_connector.Error as err:
            conn.rollback()
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise RuntimeError("Usuário/senha do MySQL inválidos.") from err
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise RuntimeError("Banco de dados não existe.") from err
            else:
                raise
        finally:
            try:
                cur.close()
            except Exception:
                pass
            conn.close()
