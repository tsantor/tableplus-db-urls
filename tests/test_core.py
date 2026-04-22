from pathlib import Path

import pytest

from tableplus.core import TableplusConfigError
from tableplus.core import build_db_url
from tableplus.core import get_local_db_conn_str
from tableplus.core import get_prod_db_conn_str


@pytest.fixture
def temp_env(tmp_path):
    """Create a temporary .env file."""
    env_file = tmp_path / "test.env"
    env_file.write_text(
        "POSTGRES_USER=user\nPOSTGRES_PASSWORD=pass\nPOSTGRES_DB=path",
        encoding="utf-8",
    )
    return env_file


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


def test_get_local_db_conn_str(temp_env):
    conn_str = get_local_db_conn_str(env_path=str(temp_env), name="Test")
    assert conn_str.startswith("postgresql://user:pass@127.0.0.1:5432/path")


def test_get_prod_db_conn_str(temp_env):
    conn_str = get_prod_db_conn_str(
        env_path=str(temp_env), name="Test", ssh_user="testuser", ssh_host="127.0.0.1"
    )
    assert conn_str.startswith(
        "postgresql+ssh://testuser@127.0.0.1/user:pass@127.0.0.1:5432/path"
    )


def test_get_local_db_conn_str_missing_env_file(tmp_path: Path):
    missing_file = tmp_path / "missing.env"
    with pytest.raises(TableplusConfigError, match="Missing local env file"):
        get_local_db_conn_str(env_path=str(missing_file), name="Test")


def test_get_prod_db_conn_str_missing_required_keys(tmp_path: Path):
    env_file = tmp_path / "production.env"
    env_file.write_text("POSTGRES_USER=user\n", encoding="utf-8")

    with pytest.raises(TableplusConfigError) as exc_info:
        get_prod_db_conn_str(
            env_path=str(env_file),
            name="Test",
            ssh_user="testuser",
            ssh_host="127.0.0.1",
        )

    assert str(env_file) in str(exc_info.value)
    assert "POSTGRES_PASSWORD" in str(exc_info.value)
    assert "POSTGRES_DB" in str(exc_info.value)
