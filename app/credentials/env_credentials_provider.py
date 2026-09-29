import os
from typing import Generic, TypeVar

from .credentials_provider import CredentialsProvider

T = TypeVar("T")


class EnvCredentialsProvider(CredentialsProvider[T], Generic[T]):
    def __init__(self, values: dict[str, str], credentials_type: type[T]):
        self._values = values
        self._credentials_type = credentials_type

    def get(self) -> T:
        credentials = {}

        for field, env_name in self._values.items():
            value = os.getenv(env_name)

            if value is None:
                raise ValueError(f"Missing environment variable '{env_name}'")

            credentials[field] = value

        return self._credentials_type(**credentials)
