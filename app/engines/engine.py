import logging

from app.config.config import load_pipeline_configs
from app.pipeline.pipeline_builder import PipelineBuilder
from app.log.logging_config import configure_logging

logger = logging.getLogger(__name__)


def main():
    configure_logging()

    logger.info("Engine started")

    pipeline_configs = load_pipeline_configs()
    builder = PipelineBuilder()

    for name, config in pipeline_configs.items():
        execution = builder.build(name, config)
        execution.run()

    logger.info("Engine finished successfully")


if __name__ == "__main__":
    main()
