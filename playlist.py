from midia import Midia
import webbrowser

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


    def cadastrarPlaylist(self):
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

        conn.close()"""  # boa sorte, se vire lucas



    

    


        

