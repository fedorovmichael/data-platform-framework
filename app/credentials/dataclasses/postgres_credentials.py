from dataclasses import dataclass

@dataclass(frozen=True)
class PostgresCredentials:
    user: str
    password: str