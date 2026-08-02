from app.config.config import load_pipeline_configs
from app.pipeline.pipeline_builder import PipelineBuilder


def main():
    pipeline_configs = load_pipeline_configs()
    print(f"pipeline configs: {pipeline_configs}")

    builder = PipelineBuilder()

    for name, config in pipeline_configs.items():
        print(f"Running pipeline: {name}")
        
        execution = builder.build(config)
        execution.run()


if __name__ == "__main__":
    main()
