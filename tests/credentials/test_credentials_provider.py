import pytest


from app.credentials.env_credentials_provider import EnvCredentialsProvider
from app.credentials.dataclasses.postgres_credentials import PostgresCredentials
from app.credentials.credentials_resolver import CredentialsResolver


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


def test_resolve_without_provider_raises_error():
    config = {
        "type": "postgres",
        "values": {
            "user": "POSTGRES1_USER",
            "password": "POSTGRES1_PASSWORD",
        },
    }

    resolver = CredentialsResolver()
    with pytest.raises(ValueError, match="The provider should be supplied."):
        resolver.resolve(config)


def test_resolve_without_type_raises_error():
    config = {
        "provider": "env",
        "values": {
            "user": "POSTGRES1_USER",
            "password": "POSTGRES1_PASSWORD",
        },
    }

    resolver = CredentialsResolver()
    with pytest.raises(ValueError, match="The type should be supplied."):
        resolver.resolve(config)


def test_resolve_without_values_raises_error():
    config = {
        "provider": "env",
        "type": "postgres",
    }

    resolver = CredentialsResolver()
    with pytest.raises(ValueError, match="The values should be supplied."):
        resolver.resolve(config)


def test_resolve_empty_provider_raises_error():
    config = {
        "provider": "",
        "type": "postgres",
        "values": {
            "user": "POSTGRES1_USER",
            "password": "POSTGRES1_PASSWORD",
        },
    }

    resolver = CredentialsResolver()
    with pytest.raises(ValueError, match="The provider should be supplied."):
        resolver.resolve(config)


def test_resolve_empty_type_raises_error():
    config = {
        "provider": "env",
        "type": "",
        "values": {
            "user": "POSTGRES1_USER",
            "password": "POSTGRES1_PASSWORD",
        },
    }

    resolver = CredentialsResolver()
    with pytest.raises(ValueError, match="The type should be supplied."):
        resolver.resolve(config)


def test_resolve_empty_values_raises_error():
    config = {"provider": "env", "type": "postgres", "values": {}}

    resolver = CredentialsResolver()
    with pytest.raises(ValueError, match="The values should be supplied."):
        resolver.resolve(config)
