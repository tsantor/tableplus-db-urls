import os
import tempfile
from argparse import Namespace

import pytest
from tableplus.core import build_db_url
from tableplus.core import get_env
from tableplus.core import get_local_db_conn_str
from tableplus.core import get_prod_db_conn_str
from tableplus.core import run

# from tableplus.core import run


@pytest.fixture(autouse=True)
def _mock_env_vars():
    # Set up mock environment variables
    os.environ["POSTGRES_USER"] = "user"
    os.environ["POSTGRES_PASSWORD"] = "pass"  # noqa: S105
    os.environ["POSTGRES_DB"] = "path"


@pytest.fixture()
def test_env():
    temp = tempfile.NamedTemporaryFile(suffix=".env", delete=False)
    temp.write(b"POSTGRES_USER=user\nPOSTGRES_PASSWORD=pass\nPOSTGRES_DB=db")
    temp.close()
    return temp


def test_build_db_url():
    params = {"foo": "bar"}
    url = build_db_url("user", "pass", "path", params=params)
    assert url == "postgresql://user:pass@127.0.0.1:5432/path?foo=bar"


def test_build_db_url_with_ssh():
    params = {"foo": "bar"}
    url = build_db_url(
        "user", "pass", "path", ssh_user="testuser", ssh_host="127.0.0.1", params=params
    )

    assert (
        url == "postgresql://testuser@127.0.0.1/user:pass@127.0.0.1:5432/path?foo=bar"
    )


def test_get_local_db_conn_str():
    env = get_env()
    conn_str = get_local_db_conn_str(env)
    assert conn_str.startswith("postgresql://user:pass@127.0.0.1:5432/path")


def test_get_prod_db_conn_str():
    env = get_env()
    conn_str = get_prod_db_conn_str(env, ssh_user="testuser", ssh_host="127.0.0.1")
    assert conn_str.startswith(
        "postgresql+ssh://testuser@127.0.0.1/user:pass@127.0.0.1:5432/path"
    )


def test_run(test_env, capsys):
    args = Namespace(path=test_env.name, user="testuser", host="127.0.0.1")
    run(args)
    captured = capsys.readouterr()
    assert isinstance(captured.out, str)
