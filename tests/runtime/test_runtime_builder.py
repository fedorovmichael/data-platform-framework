
import pytest

from app.runtime.runtime_builder import RuntimeBuilder
from app.runtime.spark_runtime import SparkRuntime


def test_return_runtime():
    config = { "type": "spark" }

    runtime = RuntimeBuilder()
    result = runtime.build(config)

    assert isinstance(result, SparkRuntime)


def test_runtime_wrong_name():
    config = { "type": "spark1" }

    runtime = RuntimeBuilder()
    with pytest.raises(ValueError, match="Unknown registry entity 'spark1'"):
        runtime.build(config)

def test_runtime_empty_config():
    config = {}

    runtime = RuntimeBuilder()
    with pytest.raises(ValueError, match="Runtime must be configured."):
        runtime.build(config)
