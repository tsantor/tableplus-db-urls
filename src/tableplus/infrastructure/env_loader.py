from pathlib import Path

from dotenv import dotenv_values

from tableplus.domain.errors import TableplusConfigError
from tableplus.domain.models import DbCredentials

REQUIRED_ENV_KEYS = ("POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB")


def load_db_credentials(env_path: str, env_name: str) -> DbCredentials:
    path = Path(env_path)
    if not path.is_file():
        raise TableplusConfigError.missing_env_file(env_name, path)

    env = dotenv_values(path)
    missing_keys = [key for key in REQUIRED_ENV_KEYS if not env.get(key)]
    if missing_keys:
        raise TableplusConfigError.missing_env_vars(env_name, path, missing_keys)

    return DbCredentials(
        username=str(env["POSTGRES_USER"]),
        password=str(env["POSTGRES_PASSWORD"]),
        database=str(env["POSTGRES_DB"]),
    )
