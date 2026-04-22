from pathlib import Path


class TableplusConfigError(ValueError):
    """Raised when required TablePlus environment configuration is missing."""

    @classmethod
    def missing_env_file(cls, env_name: str, path: Path):
        message = (
            f"Missing {env_name} env file: {path}. "
            "Expected file with POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB."
        )
        return cls(message)

    @classmethod
    def missing_env_vars(cls, env_name: str, path: Path, missing_keys: list[str]):
        missing_keys_text = ", ".join(missing_keys)
        message = (
            f"Missing required {env_name} env vars in {path}: {missing_keys_text}."
        )
        return cls(message)
