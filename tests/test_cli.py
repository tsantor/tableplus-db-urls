from pathlib import Path

import pytest
from click.testing import CliRunner

from tableplus.cli import cli


@pytest.fixture
def project_path(tmp_path):
    local_env = tmp_path / ".envs" / ".local" / ".postgres"
    prod_env = tmp_path / ".envs" / ".production" / ".postgres"
    env_content = "POSTGRES_USER=user\nPOSTGRES_PASSWORD=pass\nPOSTGRES_DB=path\n"

    local_env.parent.mkdir(parents=True, exist_ok=True)
    prod_env.parent.mkdir(parents=True, exist_ok=True)
    local_env.write_text(env_content, encoding="utf-8")
    prod_env.write_text(env_content, encoding="utf-8")
    return tmp_path


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "generate" in result.output


def test_generate_help(runner):
    result = runner.invoke(cli, ["generate", "--help"])
    assert result.exit_code == 0
    assert "--path" in result.output
    assert "--ssh-user" in result.output


def test_generate_missing_required_options(runner):
    result = runner.invoke(cli, ["generate"])
    assert result.exit_code != 0
    assert "Missing option" in result.output


def test_generate_outputs_urls(runner, project_path: Path):
    args = [
        "generate",
        "--path",
        str(project_path),
        "--name",
        "DB Name",
        "--ssh-user",
        "testuser",
        "--ssh-host",
        "127.0.0.1",
    ]
    result = runner.invoke(cli, args)

    assert result.exit_code == 0
    assert "=> TablePlus: Right click > New > Connection from URL..." in result.output
    assert "LOCAL:" in result.output
    assert "PROD:" in result.output
    assert "postgresql://user:pass@127.0.0.1:5432/path" in result.output
    assert "postgresql+ssh://testuser@127.0.0.1/user:pass@127.0.0.1:5432/path" in (
        result.output
    )


def test_generate_friendly_error_for_missing_env_file(runner, tmp_path: Path):
    result = runner.invoke(
        cli,
        [
            "generate",
            "--path",
            str(tmp_path),
            "--name",
            "DB Name",
            "--ssh-user",
            "testuser",
            "--ssh-host",
            "127.0.0.1",
        ],
    )

    assert result.exit_code != 0
    assert "Error: Missing local env file:" in result.output
    assert "Traceback" not in result.output


def test_generate_friendly_error_for_missing_required_env_vars(runner, tmp_path: Path):
    local_env = tmp_path / ".envs" / ".local" / ".postgres"
    prod_env = tmp_path / ".envs" / ".production" / ".postgres"
    local_env.parent.mkdir(parents=True, exist_ok=True)
    prod_env.parent.mkdir(parents=True, exist_ok=True)
    local_env.write_text("POSTGRES_USER=user\n", encoding="utf-8")
    prod_env.write_text("POSTGRES_USER=user\n", encoding="utf-8")

    result = runner.invoke(
        cli,
        [
            "generate",
            "--path",
            str(tmp_path),
            "--name",
            "DB Name",
            "--ssh-user",
            "testuser",
            "--ssh-host",
            "127.0.0.1",
        ],
    )

    assert result.exit_code != 0
    assert "Error: Missing required local env vars" in result.output
    assert "POSTGRES_PASSWORD" in result.output
    assert "POSTGRES_DB" in result.output
    assert "Traceback" not in result.output
