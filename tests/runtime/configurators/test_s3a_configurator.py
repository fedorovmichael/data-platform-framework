from unittest.mock import MagicMock, call
from pyspark.sql import SparkSession

from app.credentials.dataclasses.s3_credentials import S3Credentials
from app.runtime.configurators.s3a_configurator import S3AConfigurator


def test_s3a_configurator_sets_hadoop_configuration():
    hadoop_conf = MagicMock()

    spark = MagicMock(spec=SparkSession)
    spark.sparkContext._jsc.hadoopConfiguration.return_value = hadoop_conf

    configurator = S3AConfigurator(
        endpoint="http://localhost:9000",
        credentials=S3Credentials(
            access_key="test-access-key", secret_key="test-secret-key"
        ),
    )

    configurator.configure(spark)

    hadoop_conf.set.assert_has_calls(
        [
            call("fs.s3a.endpoint", "http://localhost:9000"),
            call("fs.s3a.access.key", "test-access-key"),
            call("fs.s3a.secret.key", "test-secret-key"),
            call("fs.s3a.path.style.access", "true"),
            call("fs.s3a.connection.ssl.enabled", "false"),
            call(
                "fs.s3a.aws.credentials.provider",
                "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
            ),
        ],
        any_order=False,
    )

    assert hadoop_conf.set.call_count == 6
    spark.sparkContext._jsc.hadoopConfiguration.assert_called_once_with()
