from .source_base import Source
from app.registry.source_registry import source_registry
from app.credentials.credentials_resolver import CredentialsResolver 

class SourceBuilder:
    def __init__(self):
        self._credentials_resolver = CredentialsResolver()

    def build(self, config: dict) -> Source:
        if not config:
            raise ValueError("Source must be configured.")

        options = config.get("options", {}).copy()
        credentials_config = options.pop("credentials", None)

        if credentials_config is not None:
            credentials = self._credentials_resolver.resolve(credentials_config)
            options["credentials"] = credentials

        return source_registry.create(config["type"], **options)
