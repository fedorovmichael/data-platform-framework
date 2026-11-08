from uuid import uuid4

from app.sinks.sink_s3_spark import S3SparkSink
from app.runtime.configurators.s3a_configurator import S3AConfigurator
from app.credentials.dataclasses.s3_credentials import S3Credentials


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
