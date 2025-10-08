# CMS-pra-DOOH

## Integração com pCloud

O projeto agora oferece comandos utilitários para sincronizar o arquivo de
banco de dados SQLite padrão com uma pasta no pCloud. Configure as seguintes
variáveis de ambiente antes de executar os comandos:

- `PCLOUD_EMAIL` – e-mail da conta pCloud;
- `PCLOUD_PASSWORD` – senha da conta pCloud;
- `PCLOUD_DB_REMOTE_PATH` – (opcional) caminho remoto no pCloud onde o arquivo
  deve ser armazenado, por exemplo `/backups/db.sqlite3`.

### Upload do banco para o pCloud

```bash
python manage.py pcloud_sync_db upload
```

### Download do banco do pCloud

```bash
python manage.py pcloud_sync_db download
```

Também é possível especificar um caminho remoto ou destino local diferente com
as opções `--remote-path` e `--destination`.
