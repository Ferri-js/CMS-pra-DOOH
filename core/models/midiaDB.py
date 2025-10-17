import webbrowser
import mysql.connector as mysql_connector
from mysql.connector import errorcode
from datetime import datetime

class Midia:
    def __init__(self, id, titulo, tipo, URL, dataUpload, status, duracao):
        self.id = id
        self.titulo = titulo
        self.tipo = tipo
        self.URL = URL
        self.dataUpload = dataUpload
        self.status = status
        self.duracao = duracao

    def cadastrarMidia(self):
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

            # Cria a tabela (se não existir) já com Titulo
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Midia (
                    Id_Midia INT AUTO_INCREMENT PRIMARY KEY,
                    Titulo VARCHAR(255),
                    Tipo_Midia_Id INT NOT NULL,
                    Status VARCHAR(50),
                    Duracao INT,
                    Data_Upload DATETIME,
                    URL TEXT NOT NULL,
                    UNIQUE KEY uq_midia_url (URL(255))
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # Garante a coluna Titulo mesmo se a tabela antiga existir sem ela
            cur.execute("""
                ALTER TABLE Midia
                ADD COLUMN IF NOT EXISTS Titulo VARCHAR(255)
            """)

            url = self.URL
            if not url:
                raise ValueError("URL é obrigatória para cadastrar a mídia.")

            # Deriva tipo_id (se self.tipo não for int, usa 1)
            tipo_id = self.tipo if isinstance(self.tipo, int) else 1
            status = self.status
            duracao = self.duracao
            data_upload = self.dataUpload if isinstance(self.dataUpload, datetime) else self.dataUpload
            titulo = self.titulo

            # Upsert por URL
            cur.execute("SELECT Id_Midia FROM Midia WHERE URL = %s", (url,))
            row = cur.fetchone()

            if row:
                midia_id = row[0]
                cur.execute(
                    "UPDATE Midia SET Titulo=%s, Tipo_Midia_Id=%s, Status=%s, Duracao=%s, Data_Upload=%s WHERE Id_Midia=%s",
                    (titulo, tipo_id, status, duracao, data_upload, midia_id)
                )
            else:
                cur.execute(
                    "INSERT INTO Midia (Titulo, Tipo_Midia_Id, Status, Duracao, Data_Upload, URL) VALUES (%s, %s, %s, %s, %s, %s)",
                    (titulo, tipo_id, status, duracao, data_upload, url)
                )
                midia_id = cur.lastrowid

            conn.commit()
            self.id = midia_id
            return midia_id

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

    def exibirMidia(self):
        print(f"ID: {self.id}, Título: {self.titulo}, Tipo: {self.tipo}")
        if self.URL:
            webbrowser.open(self.URL)

    def removerMidia(self):
        if not self.id:
            raise ValueError("ID da mídia não definido.")

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
            cur.execute("DELETE FROM Midia WHERE Id_Midia = %s", (self.id,))
            conn.commit()
            print(f"Mídia com ID {self.id} removida com sucesso.")
            self.id = None
        except mysql_connector.Error as err:
            conn.rollback()
            print(f"Erro ao remover mídia: {err}")
            raise
        finally:
            try:
                cur.close()
            except Exception:
                pass
            conn.close()
