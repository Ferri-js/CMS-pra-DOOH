CREATE DATABASE IF NOT EXISTS db;

CREATE TABLE Usuario (
    Id_Usuario INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255),
    Senha VARCHAR(255)
);

CREATE TABLE Tipos_Midia (
    Id_Tipo_Midia INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255)
);

CREATE TABLE Tipos_Dispositivo (
    Id_Tipo_Dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255)
);

CREATE TABLE Midia (
    Id_Midia INT AUTO_INCREMENT PRIMARY KEY,
    Tipo_Midia_Id INT,
    Tamanho INT,
    Comprimento INT,
    Largura INT,
    Status VARCHAR(255),
    Duracao INT,
    Data_Upload DATE,
    URL VARCHAR(255),
    FOREIGN KEY (Tipo_Midia_Id) REFERENCES Tipos_Midia(Id_Tipo_Midia)
);

CREATE TABLE Dispositivo (
    Id_Dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    Tipo_Dispositivo_Id INT,
    Uptime DATE,
    Status VARCHAR(255),
    Comprimento INT,
    Largura INT,
    Nome VARCHAR(255),
    Codigo_Vericacao VARCHAR(255),
    Armazenamento INT,
    FOREIGN KEY (Tipo_Dispositivo_Id) REFERENCES Tipos_Dispositivo(Id_Tipo_Dispositivo)
);

CREATE TABLE Playlist (
    id_Playlist INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Playlist VARCHAR(255)
);

CREATE TABLE Midia_Dispositivo (
    Id_MidiaDisp INT AUTO_INCREMENT PRIMARY KEY,
    Id_Midia INT,
    Id_Dispositivo INT,
    FOREIGN KEY (Id_Midia) REFERENCES Midia(Id_Midia),
    FOREIGN KEY (Id_Dispositivo) REFERENCES Dispositivo(Id_Dispositivo)
);

CREATE TABLE Midia_Playlist (
    Id_MidiaPlaylist INT AUTO_INCREMENT PRIMARY KEY,
    Id_Midia INT,
    Id_Playlist INT,
    Ordem_Midia INT,
    FOREIGN KEY (Id_Midia) REFERENCES Midia(Id_Midia),
    FOREIGN KEY (Id_Playlist) REFERENCES Playlist(id_Playlist)
);

CREATE TABLE Dispositivo_Playlist (
    Id_DispPlaylist INT AUTO_INCREMENT PRIMARY KEY,
    Id_Playlist INT,
    Id_Dispositivo INT,
    Ordem_Playlist INT,
    FOREIGN KEY (Id_Dispositivo) REFERENCES Dispositivo(Id_Dispositivo),
    FOREIGN KEY (Id_Playlist) REFERENCES Playlist(id_Playlist)
);
