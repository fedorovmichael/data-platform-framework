from .sink_base import Sink, WriteMode
from pyspark.sql import DataFrame


class S3SparkSink(Sink[DataFrame]):
    def __init__(
        self,
        bucket: str,
        path: str,
        format: str = "parquet",
        mode: str = WriteMode("append"),
        partition_by: list[str] | None = None,
    ) -> None:
        self._bucket = bucket
        self._path = path
        self._format = format
        self._mode = mode
        self._partition_by = partition_by

    def write(self, data: DataFrame) -> None:

        s3_path = f"s3a://{self._bucket}/{self._path.strip('/')}"

        writer = data.write.format(self._format).mode(self._mode)

        if self._partition_by:
            writer = writer.partitionBy(*self._partition_by)

        writer.save(s3_path)
