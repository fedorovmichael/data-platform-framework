import os

from dotenv import load_dotenv
from uuid import uuid4
from pyspark.sql import SparkSession

from app.sinks.sink_s3_spark import S3SparkSink
from app.runtime.configurators.s3a_configurator import S3AConfigurator
from app.credentials.dataclasses.s3_credentials import S3Credentials
from app.pipeline.pipeline_builder import PipelineBuilder
from app.execution.execution_status import ExecutionStatus

load_dotenv()

def test_postgres_to_s3_pipeline_end_to_end(
    postgres_test_table, postgres_source, spark_context_with_config
):

    configurator = S3AConfigurator(
        endpoint="http://localhost:9000",
        credentials=S3Credentials(
            access_key="minioadmin",
            secret_key="minioadmin123",
        ),
    )

    context = spark_context_with_config(configurator)

    source = postgres_source()

    path = f"integration-test/postgres-to-s3/{uuid4()}"

    sink = S3SparkSink(
        bucket="data-platform",
        path=path,
        format="parquet",
        mode="append",
    )

    df = source.read(context)
    sink.write(df)

    spark = context.get_resource("spark")

    result = spark.read.parquet(f"s3a://data-platform/{path}")

    rows = result.orderBy("id").collect()

    assert len(rows) == 2
    assert [row.id for row in rows] == [1, 2]
    assert [row.username for row in rows] == ["Alice", "Bob"]


def test_postgres_to_s3_pipeline_via_runtime(postgres_test_table):
    runtime_config = {
        "type": "spark",
        "options": {
            "configurators": [
                {
                    "type": "s3a",
                    "options": {
                        "endpoint": "http://localhost:9000",
                        "credentials": {
                            "provider": "env",
                            "type": "s3",
                            "values": {
                                "access_key": "MINIO_ACCESS_KEY",
                                "secret_key": "MINIO_SECRET_KEY",
                            },
                        },
                    },
                }
            ]
        },
    }

    source_config = {
        "type": "postgres_spark",
        "options": {
            "host": "localhost",
            "port": 5432,
            "database": "db_de",
            "table": postgres_test_table[0],
            "credentials": {
                "provider": "env",
                "type": "postgres",
                "values": {"user": "POSTGRES1_USER", "password": "POSTGRES1_PASSWORD"},
            },
        },
    }

    transformation_config = [
        {
            "type": "spark_select_columns",
            "options": {"columns": ["id", "username"]},
        },
        {
            "type": "spark_filter_rows",
            "options": {"condition": "id > 1"},
        },
        {"type": "spark_upper_username"},
    ]

    validators_config = [
        {"type": "spark_username_null_empty"},
        {"type": "spark_email_null_empty"},
    ]

    sink_config = {
        "type": "s3_spark",
        "options": {
            "bucket": "data-platform",
            "path": "integration-test/full-pipeline",
            "format": "parquet",
            "mode": "overwrite",
        },
    }

    pipeline_config = {
        "runtime": runtime_config,
        "source": source_config,
        "validators": validators_config,
        "transformation": transformation_config,
        "sink": sink_config,
    }

    execution = PipelineBuilder().build(
        name="postgres_to_s3_test",
        config=pipeline_config,
    )

    execution.run()

    assert execution.status == ExecutionStatus.SUCCESS

    verification_spark = (
        SparkSession.builder.master("local[2]")
        .appName("PipelineOutputVerification")
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.5.0")
        .getOrCreate()
    )

    try:
        configurator = S3AConfigurator(
            endpoint="http://localhost:9000",
            credentials=S3Credentials(
                access_key=os.environ["MINIO_ACCESS_KEY"],
                secret_key=os.environ["MINIO_SECRET_KEY"],
            ),
        ) 

        configurator.configure(verification_spark)

        result = verification_spark.read.parquet("s3a://data-platform/integration-test/full-pipeline")
        rows = result.orderBy("id").collect()

        assert len(rows) == 1
        assert rows[0].id == 2
        assert rows[0].username == "BOB"
        assert result.columns == ["id", "username"]

    finally:
        verification_spark.stop()
