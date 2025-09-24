import webbrowser

class Midia:
    def __init__(self, id, titulo, tipo, URL, dataUpload, status, duracao):
        self.id = id
        self.titulo = titulo

        self.tipo = tipo
        self.URL = URL
        self.dataUpload = dataUpload
        self.status = status
        self.duracao = duracao




    def apresentar(self):
        print(f"Olá, meu nome é {self.nome} e eu tenho {self.idade} anos.")


    #Upload | Armazenar no banco
    def cadastrarMidia():
        """import mysql.connector

        conn = mysql.connector.connect(
            host="localhost",
            user="seu_usuario",
            password="sua_senha",
            database="seu_banco"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tabela")
        for row in cursor.fetchall():
            print(row)

        conn.close()"""
        
    def exibirMidia(self):
        print(f"ID: {self.id}, Título: {self.titulo}, Tipo: {self.tipo}")
        webbrowser.open(self.URL)


        



    