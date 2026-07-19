import pytest
import json

from app.config.config import load_pipeline_configs


def test_load_single_pipeline(tmp_path):
    config = {
        "name": "orders_pipeline",
        "runtime": {"type": "spark"},
        "source": {"type": "csv"},
        "validators": [],
        "transformations": [],
        "sink": {"type": "parquet"},
    }

    (tmp_path / "single_pipeline.json").write_text(
        json.dumps(config),
        encoding="utf-8",
    )

    result = load_pipeline_configs(tmp_path)
    assert "orders_pipeline" in result
    assert result["orders_pipeline"]["name"] == "orders_pipeline"


def test_load_multiple_pipelines(tmp_path):
    orders_pipeline_config = {
        "name": "orders_pipeline",
        "runtime": {"type": "spark"},
        "source": {"type": "csv"},
        "validators": [],
        "transformations": [],
        "sink": {"type": "parquet"},
    }

    users_pipeline_config = {
        "name": "users_pipeline",
        "runtime": {"type": "spark"},
        "source": {"type": "csv"},
        "validators": [],
        "transformations": [],
        "sink": {"type": "parquet"},
    }

    (tmp_path / "orders_pipeline_config.json").write_text(
        json.dumps(orders_pipeline_config),
        encoding="utf-8",
    )

    (tmp_path / "users_pipeline_config.json").write_text(
        json.dumps(users_pipeline_config),
        encoding="utf-8",
    )

    result = load_pipeline_configs(tmp_path)
    print(f"result: {result}")
    assert "orders_pipeline" in result
    assert "users_pipeline" in result
    assert result["orders_pipeline"]["name"] == "orders_pipeline"
    assert result["users_pipeline"]["name"] == "users_pipeline"
