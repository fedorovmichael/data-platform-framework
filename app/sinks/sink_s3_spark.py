from .sink_base import Sink, WriteMode
from pyspark.sql import DataFrame


class S3SparkSink(Sink[DataFrame]):
    def __init__(
        self,
        bucket: str,
        path: str,
        format: str = "parquet",
        mode: str = WriteMode.APPEND.value,
        partition_by: list[str] | None = None,
    ) -> None:
        if not isinstance(bucket, str) or not bucket.strip():
            raise ValueError("S3 bucket must be a non-empty string.")

        if not isinstance(path, str) or not path.strip().strip("/").strip():
            raise ValueError("S3 path must be a non-empty string.")

        self._bucket = bucket
        self._path = path.strip("/")
        self._format = format
        self._mode = mode
        self._partition_by = partition_by

    def write(self, data: DataFrame) -> None:

        s3_path = f"s3a://{self._bucket}/{self._path}"

        writer = data.write.format(self._format).mode(self._mode)

        if self._partition_by:
            writer = writer.partitionBy(*self._partition_by)

        writer.save(s3_path)
