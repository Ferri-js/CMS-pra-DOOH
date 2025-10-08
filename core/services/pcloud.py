"""Utilities for interacting with the pCloud HTTP API.

This module exposes a small client tailored for synchronising the local
application database with a remote folder stored in pCloud.  The
implementation is intentionally lightweight and only relies on the
``requests`` package which is already used by the project.

The client implements the minimum subset of the API that we require:

* authenticate via e-mail/password to obtain an auth token;
* upload a file to either a folder path or a specific folder id;
* download a file from a folder path.

For security reasons every credential is read from environment variables so
that no sensitive information is committed to the repository.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class PCloudError(RuntimeError):
    """Raised when the pCloud API returns an error."""


class PCloudClient:
    """Simple wrapper around the pCloud REST API."""

    def __init__(
        self,
        *,
        email: Optional[str] = None,
        password: Optional[str] = None,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.email = email or os.getenv("PCLOUD_EMAIL")
        self.password = password or os.getenv("PCLOUD_PASSWORD")
        self.base_url = base_url or os.getenv("PCLOUD_API_BASE", "https://api.pcloud.com")
        self.session = session or requests.Session()
        self._auth_token: Optional[str] = None

        if not self.email or not self.password:
            raise ValueError(
                "Credenciais do pCloud não configuradas. Defina as variáveis "
                "de ambiente PCLOUD_EMAIL e PCLOUD_PASSWORD."
            )

    # ------------------------------------------------------------------
    # Autenticação
    # ------------------------------------------------------------------
    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, timeout=30, **kwargs)
        response.raise_for_status()
        payload = response.json()
        if payload.get("result") not in (0, None):
            raise PCloudError(payload.get("error", "Erro desconhecido ao chamar o pCloud."))
        return payload

    def authenticate(self) -> str:
        """Authenticate against the API and cache the auth token."""

        logger.debug("Autenticando no pCloud como %s", self.email)
        payload = self._request(
            "POST",
            "login",
            data={
                "getauth": 1,
                "logout": 1,
                "username": self.email,
                "password": self.password,
            },
        )
        auth = payload.get("auth")
        if not auth:
            raise PCloudError("Resposta do pCloud não contém token de autenticação.")
        self._auth_token = auth
        logger.debug("Autenticação bem-sucedida. Token recebido.")
        return auth

    # ------------------------------------------------------------------
    # Upload e download de arquivos
    # ------------------------------------------------------------------
    def ensure_auth(self) -> str:
        if self._auth_token:
            return self._auth_token
        return self.authenticate()

    def upload_file(
        self,
        local_path: Path | str,
        *,
        remote_path: Optional[str] = None,
        folder_id: Optional[int] = None,
        overwrite: bool = True,
    ) -> dict:
        """Upload a file to pCloud and return the API payload."""

        auth = self.ensure_auth()
        path_obj = Path(local_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Arquivo local {path_obj} não encontrado.")

        params = {"auth": auth, "nopartial": 1, "renameifexists": 0}
        if not overwrite:
            params["renameifexists"] = 1
        if folder_id is not None:
            params["folderid"] = folder_id
            params["filename"] = path_obj.name
        else:
            params["path"] = remote_path or f"/{path_obj.name}"

        logger.info("Enviando %s para o pCloud (destino: %s)", path_obj, params.get("path", folder_id))
        with path_obj.open("rb") as file_handle:
            files = {"file": (path_obj.name, file_handle)}
            payload = self._request("POST", "uploadfile", params=params, files=files)
        logger.info("Upload concluído com sucesso.")
        return payload

    def download_file(self, *, remote_path: str, destination: Path | str) -> Path:
        """Download a file from pCloud and save it locally."""

        auth = self.ensure_auth()
        params = {"auth": auth, "path": remote_path, "timeformat": "timestamp"}
        logger.info("Baixando %s do pCloud", remote_path)
        payload = self._request("GET", "getfilelink", params=params)
        hosts = payload.get("hosts", [])
        path = payload.get("path")
        if not hosts or not path:
            raise PCloudError("Resposta do pCloud não contém link de download válido.")

        # A URL de download é composta pelo host retornado + path + auth
        download_url = f"https://{hosts[0]}{path}?auth={auth}"
        response = self.session.get(download_url, stream=True, timeout=60)
        response.raise_for_status()

        destination_path = Path(destination)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        with destination_path.open("wb") as output:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output.write(chunk)

        logger.info("Download concluído: %s", destination_path)
        return destination_path


def default_database_path() -> Path:
    """Return the path of the default Django database file."""

    base_dir = Path(os.getenv("DJANGO_BASE_DIR", Path(__file__).resolve().parents[2]))
    return base_dir / "db.sqlite3"


def upload_default_database(*, client: Optional[PCloudClient] = None, remote_path: Optional[str] = None) -> dict:
    """Upload the default SQLite database to pCloud."""

    db_path = default_database_path()
    client = client or PCloudClient()
    remote = remote_path or os.getenv("PCLOUD_DB_REMOTE_PATH", f"/backups/{db_path.name}")
    return client.upload_file(db_path, remote_path=remote)


def download_default_database(
    *,
    client: Optional[PCloudClient] = None,
    remote_path: Optional[str] = None,
    destination: Optional[Path | str] = None,
) -> Path:
    """Download the default SQLite database from pCloud."""

    db_path = destination or default_database_path()
    client = client or PCloudClient()
    remote = remote_path or os.getenv("PCLOUD_DB_REMOTE_PATH", f"/backups/{Path(db_path).name}")
    return client.download_file(remote_path=remote, destination=db_path)
