import logging
from pathlib import Path

import click

from tableplus.application.connection_strings import get_local_db_conn_str
from tableplus.application.connection_strings import get_prod_db_conn_str
from tableplus.domain.errors import TableplusConfigError

logger = logging.getLogger(__name__)


@click.command()
@click.option("-p", "--path", required=True, help="Path to the project")
@click.option("-n", "--name", required=True, help="TablePlus Connection Name")
@click.option("--ssh-user", required=True, help="SSH User")
@click.option("--ssh-host", required=True, help="SSH Host")
def generate(path, name, ssh_user, ssh_host) -> None:
    """Main entry point for the CLI."""

    project_path = Path(path).expanduser()
    local_env_path = str(project_path / ".envs/.local/.postgres")
    prod_env_path = str(project_path / ".envs/.production/.postgres")

    try:
        local_db_url = get_local_db_conn_str(env_path=local_env_path, name=name)
        prod_db_url = get_prod_db_conn_str(
            env_path=prod_env_path, name=name, ssh_user=ssh_user, ssh_host=ssh_host
        )
    except TableplusConfigError as exc:
        raise click.ClickException(str(exc)) from exc

    click.secho("=> TablePlus: Right click > New > Connection from URL...", fg="green")
    click.secho("\nLOCAL:", dim=True)
    click.secho(f"{local_db_url}")
    click.secho("\nPROD:", dim=True)
    click.secho(f"{prod_db_url}")


# Set up your command-line interface grouping
@click.group()
@click.version_option(package_name="tableplus-db-urls", prog_name="tableplus-db-urls")
def cli():
    """Generate TablePlus DB URLs from .env files for local and production environments."""


cli.add_command(generate)

if __name__ == "__main__":
    cli()
