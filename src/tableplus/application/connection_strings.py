from tableplus.domain.urls import build_db_url
from tableplus.infrastructure.env_loader import load_db_credentials

LOCAL_PARAMS = {
    "statusColor": "DAEBC2",
    "env": "local",
    "name": "",
    "lazyload": "true",
}

PROD_PARAMS = {
    "statusColor": "FFD7D4",
    "env": "production",
    "name": "",
    "tLSMode": "0",
    "usePrivateKey": "true",
    "lazyload": "true",
}


def get_local_db_conn_str(env_path, name: str) -> str:
    """Get the local DB connection string."""
    credentials = load_db_credentials(str(env_path), "local")
    params = {**LOCAL_PARAMS, "name": name}

    return build_db_url(
        credentials.username,
        credentials.password,
        credentials.database,
        params=params,
    )


def get_prod_db_conn_str(env_path, name: str, ssh_user: str, ssh_host: str) -> str:
    """Get the production DB connection string."""
    credentials = load_db_credentials(str(env_path), "production")
    params = {**PROD_PARAMS, "name": name}

    return build_db_url(
        credentials.username,
        credentials.password,
        credentials.database,
        params=params,
        scheme="postgresql+ssh",
        ssh_user=ssh_user,
        ssh_host=ssh_host,
    )
