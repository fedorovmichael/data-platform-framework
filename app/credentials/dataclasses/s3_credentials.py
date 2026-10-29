from dataclasses import dataclass

@dataclass(frozen=True)
class S3Credentials:
    access_key: str
    secret_key: str