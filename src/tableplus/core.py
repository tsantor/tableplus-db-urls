from argparse import Namespace
from pathlib import Path
from urllib.parse import quote
from urllib.parse import urlencode

# from urllib.parse import quote_plus
import environ

env = environ.Env()


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


def get_local_db_conn_str(env_path: str) -> str:
    """Get the local DB connection string."""
    env.read_env(env_path)

    params = {
        "statusColor": "F8F8F8",
        "env": "local",
        "name": "USTA",
        "lazyload": "true",
    }

    db_user = env("POSTGRES_USER")
    db_pass = env("POSTGRES_PASSWORD")
    db_name = env("POSTGRES_DB")

    return build_db_url(db_user, db_pass, db_name, params=params)


def get_prod_db_conn_str(env_path: str, ssh_user: str, ssh_host: str) -> str:
    """Get the production DB connection string."""
    env.read_env(env_path)

    params = {
        "statusColor": "FFD7D4",
        "env": "production",
        "name": "USTA [TEST]",
        "tLSMode": "0",
        "usePrivateKey": "true",
        # "safeModeLevel": "0",
        # "advancedSafeModeLevel": "0",
        # "driverVersion": "0",
        "lazyload": "true",
    }

    db_user = env("POSTGRES_USER")
    db_pass = env("POSTGRES_PASSWORD")
    db_name = env("POSTGRES_DB")

    return build_db_url(
        db_user,
        db_pass,
        db_name,
        params=params,
        scheme="postgresql+ssh",
        ssh_user=ssh_user,
        ssh_host=ssh_host,
    )


def run(args: Namespace):
    """Main entry point for the CLI."""
    project_path = Path(args.path).expanduser()
    local_env_path = str(project_path / ".envs/.local/.postgres")
    prod_env_path = str(project_path / ".envs/.production/.postgres")

    print("LOCAL DB CONN:", get_local_db_conn_str(local_env_path))  # noqa: T201
    print(
        "PROD DB CONN:",
        get_prod_db_conn_str(prod_env_path, args.user, args.host),
    )  # noqa: T201
