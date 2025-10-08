"""Management command to synchronise the local database with pCloud."""

from __future__ import annotations
import logging
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandParser, CommandError

from core.services.pcloud import (
    download_default_database,
    upload_default_database,
    PCloudError,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sincroniza o arquivo de banco de dados local com o pCloud."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "direction",
            choices=("upload", "download"),
            help="Direção da sincronização: 'upload' envia o banco local para o pCloud, "
            "'download' baixa o arquivo do pCloud para a máquina local.",
        )
        parser.add_argument(
            "--remote-path",
            dest="remote_path",
            help="Caminho remoto a ser utilizado no pCloud. Por padrão usa o valor da "
            "variável de ambiente PCLOUD_DB_REMOTE_PATH ou /backups/db.sqlite3.",
        )
        parser.add_argument(
            "--destination",
            dest="destination",
            type=Path,
            help="Destino local para salvar o arquivo quando a direção for 'download'.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        direction: str = options["direction"]
        remote_path: str | None = options.get("remote_path")
        destination: Path | None = options.get("destination")

        try:
            if direction == "upload":
                payload = upload_default_database(remote_path=remote_path)
                self.stdout.write(self.style.SUCCESS("Upload concluído."))
                self.stdout.write(self._format_payload(payload))
            else:
                path = download_default_database(remote_path=remote_path, destination=destination)
                self.stdout.write(self.style.SUCCESS(f"Download concluído: {path}"))
        except (ValueError, PCloudError, OSError) as exc:
            logger.exception("Falha ao sincronizar com o pCloud: %s", exc)
            raise CommandError(str(exc)) from exc

    def _format_payload(self, payload: dict | None) -> str:
        if not payload:
            return "Nenhuma informação adicional retornada pelo pCloud."

        lines = ["Detalhes da resposta do pCloud:"]
        for key, value in payload.items():
            lines.append(f"  - {key}: {value}")
        return "\n".join(lines)
