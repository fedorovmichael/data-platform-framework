import json
from pathlib import Path
from typing import Any

CONFIG_PIPELINES_DIR = Path(__file__).parent / "pipelines"


def load_pipeline_configs(
    pipelines_dir: Path = CONFIG_PIPELINES_DIR,
) -> dict[str, dict[str, Any]]:
    if not pipelines_dir.exists():
        raise FileNotFoundError(
            f"Configuration directtory does not exist: {pipelines_dir}"
        )

    if not pipelines_dir.is_dir():
        raise NotADirectoryError(
            f"Configuration path is not a directory: {pipelines_dir}"
        )

    pipeline_configs: dict[str, dict[str, Any]] = {}

    for config_path in sorted(pipelines_dir.glob("*.json")):
        config_data = _load_json_file(config_path)

        pipeline_name = config_data.get("name")

        if not isinstance(pipeline_name, str) or not pipeline_name.strip():
            raise ValueError(
                f"Configuration file '{config_path.name}' "
                "must contain a non-empty string field 'name'"
            )

        if pipeline_name in pipeline_configs:
            raise ValueError(
                f"Duplicate pipeline name '{pipeline_name}' "
                f"in file '{config_path.name}'"
            )

        pipeline_configs[pipeline_name] = config_data

    return pipeline_configs


def _load_json_file(config_path: Path) -> dict[str, Any]:
    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in '{config_path.name}': "
            f"line {error.lineno}, column {error.colno}: {error.msg}"
        ) from error

    if not isinstance(config_data, dict):
        raise ValueError(
            f"Configuration root in '{config_path}' must be a JSON object."
        )

    return config_data
