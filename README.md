# Nexxo - CMS para DOOH

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.0+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Nexxo** é uma plataforma web de gerenciamento de conteúdo (CMS) desenvolvida especificamente para **Digital Out-of-Home (DOOH)**. O sistema permite o controle centralizado de mídias, playlists e dispositivos de exibição digital.

>  Projeto desenvolvido como parte do **First Steps** da **PUC TECH** - Liga Acadêmica de Tecnologia da PUC.

---

##  Funcionalidades

-  **Gerenciamento de Dispositivos** - Cadastro e controle de telas e dispositivos DOOH
-  **Gestão de Mídias** - Upload e organização de vídeos, imagens e conteúdo multimídia
-  **Playlists Inteligentes** - Criação e agendamento de playlists para exibição
-  **Integração pCloud** - Armazenamento em nuvem para mídias
  
---

## 🛠️ Tecnologias

- **Backend:** Django
- **Banco de Dados:** MySQL
- **ORM:** Django ORM
- **Cloud Storage:** pCloud API
- **Frontend:** Django Templates (HTML + HTMX)

---

## 📋 Pré-requisitos

- Python 
- MySQL 

```
CMS-para-DOOH/
│
├── models/
│   ├── midia.py              # Model de Mídia
│   ├── dispositivo.py        # Model de Dispositivo
│   ├── playlist.py           # Model de Playlist
│   └── ...
│
├── database/
│   └── schema.sql            # Script SQL do banco
│
├── static/
│   └── ...                   # Arquivos estáticos
│
├── templates/
│   └── ...                   # Templates HTML
│
├── requirements.txt          # Dependências Python
├── manage.py                 # CLI Django
└── README.md                 # Este arquivo
```

---

## 🗄️ Modelos do Banco de Dados

### Principais Entidades

- **Midia** - Armazena vídeos, imagens e outros conteúdos
- **Dispositivo** - Representa telas e displays DOOH
- **Playlist** - Agrupa mídias em sequências de reprodução
- **TipoMidia** / **TipoDispositivo** - Categorização de tipos
- **MidiaPlaylist** - Relação N:N entre Mídia e Playlist
- **DispositivoPlaylist** - Relação N:N entre Dispositivo e Playlist

---


**PUC TECH** - Liga Acadêmica de Tecnologia da PUC

Projeto First Steps 2024/2025
