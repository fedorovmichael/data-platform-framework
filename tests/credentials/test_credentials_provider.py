import pytest


from app.credentials.env_credentials_provider import EnvCredentialsProvider
from app.credentials.dataclasses.postgres_credentials import PostgresCredentials


def test_get_env_credentials_success(monkeypatch):
    monkeypatch.setenv("POSTGRES1_USER", "test_user")
    monkeypatch.setenv("POSTGRES1_PASSWORD", "test_password")

    provider = EnvCredentialsProvider(
        values={
            "user": "POSTGRES1_USER",
            "password": "POSTGRES1_PASSWORD",
        },
        credentials_type=PostgresCredentials,
    )

    credentials = provider.get()

    assert isinstance(credentials, PostgresCredentials)
    assert credentials.user == "test_user"
    assert credentials.password == "test_password"


def test_get_postgres_credentials_missing_password(monkeypatch):
    monkeypatch.setenv("POSTGRES1_USER", "test_user")
    monkeypatch.delenv("POSTGRES1_PASSWORD", raising=False)

    provider = EnvCredentialsProvider(
        values={
            "user": "POSTGRES1_USER",
            "password": "POSTGRES1_PASSWORD",
        },
        credentials_type=PostgresCredentials,
    )

    with pytest.raises(ValueError) as exc_info:
        provider.get()

    assert "POSTGRES1_PASSWORD" in str(exc_info.value)
