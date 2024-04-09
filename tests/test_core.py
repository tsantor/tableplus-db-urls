import os

import pytest
from tableplus.core import build_db_url
from tableplus.core import get_local_db_conn_str
from tableplus.core import get_prod_db_conn_str

# from tableplus.core import run


@pytest.fixture(autouse=True)
def _mock_env_vars():
    # Set up mock environment variables
    os.environ["POSTGRES_USER"] = "user"
    os.environ["POSTGRES_PASSWORD"] = "pass"  # noqa: S105
    os.environ["POSTGRES_DB"] = "path"


def test_build_db_url():
    url = build_db_url("user", "pass", "path")
    assert url == "postgresql://user:pass@127.0.0.1:5432/path"


def test_build_db_url_with_ssh():
    url = build_db_url("user", "pass", "path", ssh_user="ssh_user", ssh_host="ssh_host")
    assert url == "postgresql://ssh_user@ssh_host/user:pass@127.0.0.1:5432/path"


def test_get_local_db_conn_str():
    conn_str = get_local_db_conn_str(".env")
    assert conn_str.startswith("postgresql://user:pass@127.0.0.1:5432/path")


def test_get_prod_db_conn_str():
    conn_str = get_prod_db_conn_str(".env", ssh_user="usta", ssh_host="159.203.98.10")
    assert conn_str.startswith(
        "postgresql+ssh://usta@159.203.98.10/user:pass@127.0.0.1:5432/path"
    )
