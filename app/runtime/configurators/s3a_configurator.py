from pyspark.sql import SparkSession

from .configurator_base import SparkConfigurator
from app.credentials.dataclasses.s3_credentials import S3Credentials


class S3AConfigurator(SparkConfigurator):
    def __init__(self, endpoint: str, credentials: S3Credentials) -> None:
        self._endpoint = endpoint
        self._credentials = credentials

    def configure(self, spark: SparkSession) -> None:
        hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

        hadoop_conf.set("fs.s3a.endpoint", self._endpoint)
        hadoop_conf.set(
            "fs.s3a.access.key",
            self._credentials.access_key,
        )
        hadoop_conf.set(
            "fs.s3a.secret.key",
            self._credentials.secret_key,
        )
        hadoop_conf.set("fs.s3a.path.style.access", "true")
        hadoop_conf.set("fs.s3a.connection.ssl.enabled", "false")
        hadoop_conf.set(
            "fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        )
