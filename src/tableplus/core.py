from pathlib import Path
from urllib.parse import quote
from urllib.parse import urlencode

from dotenv import dotenv_values

REQUIRED_ENV_KEYS = ("POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB")


class TableplusConfigError(ValueError):
    """Raised when required TablePlus environment configuration is missing."""

    @classmethod
    def missing_env_file(cls, env_name: str, path: Path):
        message = (
            f"Missing {env_name} env file: {path}. "
            "Expected file with POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB."
        )
        return cls(message)

    @classmethod
    def missing_env_vars(cls, env_name: str, path: Path, missing_keys: list[str]):
        missing_keys_text = ", ".join(missing_keys)
        message = (
            f"Missing required {env_name} env vars in {path}: {missing_keys_text}."
        )
        return cls(message)


def _load_db_credentials(env_path: str, env_name: str) -> tuple[str, str, str]:
    path = Path(env_path)
    if not path.is_file():
        raise TableplusConfigError.missing_env_file(env_name, path)

    env = dotenv_values(path)
    missing_keys = [key for key in REQUIRED_ENV_KEYS if not env.get(key)]
    if missing_keys:
        raise TableplusConfigError.missing_env_vars(env_name, path, missing_keys)

    return (
        str(env["POSTGRES_USER"]),
        str(env["POSTGRES_PASSWORD"]),
        str(env["POSTGRES_DB"]),
    )


def build_db_url(  # noqa: PLR0913
    username: str,
    password: str,
    path: str,
    scheme: str = "postgresql",
    host: str = "127.0.0.1",
    port: int = 5432,
    params: dict[str, str] = None,  # noqa: RUF013
    ssh_user=None,
    ssh_host=None,
) -> str:
    """Build a DB URL."""
    path = f"/{path}" if not path.startswith("/") else path.rstrip("/")
    query_string = urlencode(params or {}, quote_via=quote)
    ssh = f"{ssh_user}@{ssh_host}/" if ssh_user and ssh_host else ""

    return (
        f"{scheme}://{ssh}{username}:{password}@{host}:{port}{path}?"
        f"{query_string}".rstrip("?")
    )


def get_local_db_conn_str(env_path, name: str) -> str:
    """Get the local DB connection string."""
    params = {
        "statusColor": "DAEBC2",
        "env": "local",
        "name": name,
        "lazyload": "true",
    }

    db_user, db_pass, db_name = _load_db_credentials(str(env_path), "local")

    return build_db_url(db_user, db_pass, db_name, params=params)


def get_prod_db_conn_str(env_path, name: str, ssh_user: str, ssh_host: str) -> str:
    """Get the production DB connection string."""
    params = {
        "statusColor": "FFD7D4",
        "env": "production",
        "name": name,
        "tLSMode": "0",
        "usePrivateKey": "true",
        # "safeModeLevel": "0",
        # "advancedSafeModeLevel": "0",
        # "driverVersion": "0",
        "lazyload": "true",
    }
    db_user, db_pass, db_name = _load_db_credentials(str(env_path), "production")

    return build_db_url(
        db_user,
        db_pass,
        db_name,
        params=params,
        scheme="postgresql+ssh",
        ssh_user=ssh_user,
        ssh_host=ssh_host,
    )
