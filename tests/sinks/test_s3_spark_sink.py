import pytest

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


def test_s3_sink_normallizes_path():
    sink = S3SparkSink(
        bucket="data-platform",
        path="/output/users/",
    )

    assert sink._path == "output/users"
