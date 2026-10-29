from .registry_base import EntityRegistry

from app.credentials.credentials_provider import CredentialsProvider
from app.credentials.dataclasses.postgres_credentials import PostgresCredentials
from app.credentials.env_credentials_provider import EnvCredentialsProvider
from app.credentials.dataclasses.s3_credentials import S3Credentials

credentials_provider_registry = EntityRegistry[CredentialsProvider]()
credentials_provider_registry.register("env", EnvCredentialsProvider)

credentials_type_registry = EntityRegistry()
credentials_type_registry.register("postgres", PostgresCredentials)
credentials_type_registry.register("s3", S3Credentials)