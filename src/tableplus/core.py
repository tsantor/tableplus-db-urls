from argparse import Namespace
from pathlib import Path
from urllib.parse import quote
from urllib.parse import urlencode

import environ

# from urllib.parse import quote_plus


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


def get_env(env_path=None) -> environ.Env:
    """Get the environment variables."""
    env = environ.Env()
    if env_path and Path(env_path).exists():
        env.read_env(env_path)
    return env


def get_local_db_conn_str(env: environ.Env) -> str:
    """Get the local DB connection string."""
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


def get_prod_db_conn_str(env: environ.Env, ssh_user: str, ssh_host: str) -> str:
    """Get the production DB connection string."""
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


def _output_db_urls(local_db_url: str, prod_db_url: str) -> None:
    """Output the DB URLs."""
    print("=> TablePlus: Right click > New > Connection from URL...")  # noqa: T201
    print("LOCAL:", local_db_url)  # noqa: T201
    print("PROD:", prod_db_url)  # noqa: T201


def run(args: Namespace) -> None:
    """Main entry point for the CLI."""
    project_path = Path(args.path).expanduser()
    local_env_path = str(project_path / ".envs/.local/.postgres")
    prod_env_path = str(project_path / ".envs/.production/.postgres")

    local_env = get_env(local_env_path)
    prod_env = get_env(prod_env_path)

    local_db_url = get_local_db_conn_str(local_env)
    prod_db_url = get_prod_db_conn_str(prod_env, args.user, args.host)

    _output_db_urls(local_db_url, prod_db_url)
