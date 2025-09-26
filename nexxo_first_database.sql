/* Logico_cms_playlist: */
create database db;

CREATE TABLE Usuario (
    Id_Usuario int PRIMARY KEY,
    Email Varchar(255),
    Senha Varchar(255)
);

CREATE TABLE Midia (
    Id_Midia int PRIMARY KEY,
    Tipo_Midia_Id int,
    Tamanho int,
    Comprimento int,
    Largura int,
    Status Varchar(255),
    Duracao int,
    Data_Upload date,
    URL Varchar(255)
);

CREATE TABLE Dispositivo (
    Id_Dispositivo int PRIMARY KEY,
    Tipo_Dispositivo_Id int,
    Uptime date,
    Status Varchar(255),
    Comprimento int,
    Largura int,
    Nome Varchar(255),
    Codigo_Vericacao Varchar(255),
    Armazenamento INT
);

CREATE TABLE Tipos_Midia (
    Id_Tipo_Midia int PRIMARY KEY,
    Nome Varchar(255)
);

CREATE TABLE Tipos_Dispositivo (
    Id_Tipo_Dispositivo int PRIMARY KEY,
    Nome Varchar(255)
);

CREATE TABLE Midia_Dispositivo_Recebe (
    Id_MidiaDisp int PRIMARY KEY,
    Id_Midia int,
    Id_Dispositivo int
);

CREATE TABLE Playlist (
	id_Playlist int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Nome_Playlist Varchar(255)
);

CREATE TABLE Midia_Playlist_Compoe (
    Id_MidiaPlaylist int PRIMARY KEY,
    Id_Midia int,
    Id_Playlist int,
    Ordem_Midia int
);

CREATE TABLE Dispositivo_Playlist_Exibe (
    Id_DispPlaylist int PRIMARY KEY,
    Id_Playlist int,
    Id_Dispositivo int,
    Ordem_Playlist int
);
 
ALTER TABLE Midia ADD CONSTRAINT FK_Midia_Tipo
	FOREIGN KEY (Tipo_Midia_Id)
    REFERENCES Tipos_Midia (Id_Tipo_Midia);
 
ALTER TABLE Dispositivo ADD CONSTRAINT FK_Dispositivo_Tipo
    FOREIGN KEY (Tipo_Dispositivo_Id)
    REFERENCES Tipos_Dispositivo (Id_Tipo_Dispositivo);
 
ALTER TABLE Midia_Dispositivo_Recebe ADD CONSTRAINT FK_Midia_Dispositivo_Recebe_Midia
    FOREIGN KEY (Id_Midia)
    REFERENCES Midia (Id_Midia);

ALTER TABLE Midia_Dispositivo_Recebe ADD CONSTRAINT FK_Midia_Dispositivo_Recebe_Dispositivo
    FOREIGN KEY (Id_Dispositivo)
    REFERENCES Dispositivo (Id_Dispositivo);
 
ALTER TABLE Midia_Playlist_Compoe ADD CONSTRAINT FK_Midia_Playlist_Midia
    FOREIGN KEY (Id_Midia)
    REFERENCES Midia (Id_Midia);

ALTER TABLE Midia_Playlist_Compoe ADD CONSTRAINT FK_Midia_Playlist_Playlist
    FOREIGN KEY (Id_Playlist)
    REFERENCES Playlist (id_Playlist);
 
ALTER TABLE Dispositivo_Playlist_Exibe ADD CONSTRAINT FK_Disp_Playlist_Disp
    FOREIGN KEY (Id_Dispositivo)
    REFERENCES Dispositivo (Id_Dispositivo);

ALTER TABLE Dispositivo_Playlist_Exibe ADD CONSTRAINT FK_Disp_Playlist_Playlist
    FOREIGN KEY (Id_Playlist)
    REFERENCES Playlist (id_Playlist);
    
RENAME TABLE Midia_Playlist_Compoe TO Midia_Playlist;
RENAME TABLE Dispositivo_Playlist_Exibe TO Dispositivo_Playlist;
RENAME TABLE Midia_Dispositivo_Recebe TO Midia_Dispositivo;

ALTER TABLE Playlist MODIFY id_Playlist INT AUTO_INCREMENT PRIMARY KEY;