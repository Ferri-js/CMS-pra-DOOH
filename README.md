# Nexxo - CMS para DOOH

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.0+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)

**Nexxo** é uma plataforma web de gerenciamento de conteúdo (CMS) para **Digital Out-of-Home (DOOH)**. Permite o controle centralizado de mídias, playlists e dispositivos de exibição digital.

Projeto desenvolvido como parte do **First Steps** da **PUC TECH** - Liga Acadêmica de Tecnologia da PUC.

---

## Funcionalidades

- Gerenciamento de dispositivos DOOH
- Upload e organização de mídias (vídeo, imagem, HTML)
- Criação de playlists com ordenação
- Integração com Supabase para armazenamento em nuvem
- Sistema de autenticação
- Player web com reprodução em loop

## Tecnologias

- Backend: Django 4.2+
- Banco de Dados: MySQL 8.0+
- Cloud Storage: Supabase
- Frontend: Django Templates + HTMX
- Hospedagem: PythonAnywhere

---

### Páginas Principais

- **Login:** [https://danielteles.pythonanywhere.com/login/](https://danielteles.pythonanywhere.com/login/)
- **Painel de Gerenciamento:** [https://danielteles.pythonanywhere.com/gerenciar/](https://danielteles.pythonanywhere.com/gerenciar/)
- **Verificação de Dispositivo:** [https://danielteles.pythonanywhere.com/verificar/](https://danielteles.pythonanywhere.com/verificar/)

---

## Como Usar

### 1. Fazer Login
- Acesse [/login/](https://danielteles.pythonanywhere.com/login/)

### 2. Adicionar Mídias
- Acesse o Painel de Gerenciamento
- Na coluna "Acervo de Mídias", faça upload de vídeos/imagens ou cole URLs HTML
- A mídia será automaticamente enviada ao Supabase

### 3. Criar Playlist
- Na coluna "Playlists", crie uma nova playlist
- Marque "Ativa" para disponibilizá-la aos dispositivos
- Clique na playlist para adicionar mídias

### 4. Configurar Dispositivos
- Na coluna "Dispositivos", cadastre um novo dispositivo
- Defina um código de verificação único
- Associe uma playlist ativa

### 5. Acessar o Player
- No dispositivo físico, acesse [/verificar/](https://danielteles.pythonanywhere.com/verificar/)
- Insira o código de verificação
- O player iniciará automaticamente

---

## Estrutura do Banco

### Midia
- `titulo` - Nome da mídia
- `tipo` - VIDEO | IMAGEM | HTML
- `url_publica` - URL do Supabase
- `duracao` - Tempo de exibição (segundos)

### Playlist
- `titulo` - Nome da playlist
- `ativa` - Status (booleano)

### ItemPlaylist
- `playlist` - FK para Playlist
- `midia` - FK para Midia
- `ordem` - Posição na sequência

### Dispositivo
- `nomeDispositivo` - Nome do dispositivo
- `codVerificacao` - Código único de acesso
- `playlistAssociada` - FK para Playlist

---

## Instalação Local (Desenvolvimento)

Para rodar o projeto localmente:

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/nexxo-cms.git
cd nexxo-cms
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Configure o `.env` com credenciais do MySQL e Supabase

4. Execute as migrações
```bash
python manage.py migrate
```

5. Inicie o servidor
```bash
python manage.py runserver
```

---

## Troubleshooting

**Mídia não aparece no player**
- Verifique se `url_publica` está preenchida no banco
- Confirme que a playlist está marcada como "Ativa"
- Teste a URL diretamente no navegador

**Erro ao fazer login**
- Verifique as credenciais com a equipe
- Caso necessário, crie um novo superusuário via Django Admin

**Player não inicia**
- Confirme que o dispositivo tem uma playlist associada
- Verifique se a playlist contém pelo menos uma mídia

---
