from app.registry.runtime_registry import spark_configurator_registry 
from app.credentials.credentials_resolver import CredentialsResolver
from app.runtime.configurators.configurator_builder import SparkConfigurator


class SparkConfiguratorBuilder:
    def build(self, config: dict) -> SparkConfigurator:
        if not config:
            raise ValueError("Spark configurator must be configured.")

        options = config.get("options", {}).copy()

        credentials_config = options.pop("credentials", None)

        if credentials_config:
            credentials = CredentialsResolver.resolve(credentials_config)
            options["credentials"] = credentials

        return spark_configurator_registry.create(
            config["type"],
            **options,
        )