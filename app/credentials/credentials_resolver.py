from app.registry.credential_registry import (
    credentials_provider_registry,
    credentials_type_registry,
)


class CredentialsResolver:
    def resolve(self, config: dict):
        if not config.get("provider"):
            raise ValueError("The provider should be supplied.")

        if not config.get("type"):
            raise ValueError("The type should be supplied.")

        if not config.get("values"):
            raise ValueError("The values should be supplied.")

        credentials_type = credentials_type_registry.get(config["type"])
        provider = credentials_provider_registry.create(
            config["provider"],
            values=config["values"],
            credentials_type=credentials_type,
        )
        return provider.get()
