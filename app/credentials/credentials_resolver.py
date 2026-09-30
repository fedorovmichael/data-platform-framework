from app.registry.credential_registry import credentials_provider_registry, credentials_type_registry 

credentials_type = credentials_type_registry.get("postgres")
provider = credentials_provider_registry.create(
    "env",
    values={
        "user": "POSTGRES1_USER",
        "password": "POSTGRES1_PASSWORD",
    },
    credentials_type=credentials_type,
)
credentials = provider.get()