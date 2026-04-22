from dataclasses import dataclass


@dataclass(frozen=True)
class DbCredentials:
    username: str
    password: str
    database: str
