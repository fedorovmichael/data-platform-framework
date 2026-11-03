import pytest

from unittest.mock import MagicMock
from pyspark.sql import DataFrame

from app.sinks.sink_s3_spark import S3SparkSink


@pytest.mark.parametrize(
    "bucket",
    ["", " ", None],
)
def test_s3_sink_invalid_bucket(bucket):
    with pytest.raises(ValueError, match="S3 bucket must be a non-empty string."):
        S3SparkSink(bucket, path="output/users")


@pytest.mark.parametrize("path", ["", " ", "/", "///", None])
def test_s3_sink_invalid_path(path):
    with pytest.raises(ValueError, match="S3 path must be a non-empty string."):
        S3SparkSink(bucket="data-platform", path=path)


def test_s3_sink_normalizes_path():
    sink = S3SparkSink(
        bucket="data-platform",
        path="/output/users/",
    )

    assert sink._path == "output/users"


def test_s3_sink_write_with_partitions():
    df = MagicMock(spec=DataFrame)

    writer = MagicMock()
    writer.format.return_value = writer
    writer.mode.return_value = writer
    writer.partitionBy.return_value = writer

    df.write = writer

    sink = S3SparkSink(
        bucket="data-platform",
        path="output/users",
        format="parquet",
        mode="append",
        partition_by=["year", "month"],
    )

    sink.write(df)

    writer.format.assert_called_once_with("parquet")
    writer.mode.assert_called_once_with("append")
    writer.partitionBy.assert_called_once_with("year", "month")
    writer.save.assert_called_once_with("s3a://data-platform/output/users")



def test_s3_sink_write_without_partitions():
    df = MagicMock(spec=DataFrame)

    writer = MagicMock()
    writer.format.return_value = writer
    writer.mode.return_value = writer
    writer.partitionBy.return_value = writer

    df.write = writer

    sink = S3SparkSink(
        bucket="data-platform",
        path="output/users",
    )

    sink.write(df)

    writer.format.assert_called_once_with("parquet")
    writer.mode.assert_called_once_with("append")
    writer.partitionBy.assert_not_called()
    writer.save.assert_called_once_with("s3a://data-platform/output/users")
