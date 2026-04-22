from urllib.parse import quote
from urllib.parse import urlencode


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
