from app.pipeline.pipeline_builder import PipelineBuilder


def test_csv_to_parquet_pipeline(tmp_path):
    input_path = tmp_path / "users.csv"
    output_path = tmp_path / "users.parquet"

    input_path.write_text(
        "id,username,email\n" "1,alice,alice@example.com\n" "2,bob,bob@example.com\n"
    )

    config = {
        "name": "user_pipeline",
        "runtime": {"type": "spark"},
        "enabled": True,
        "source": {"type": "csv_spark", "options": {"path": str(input_path)}},
        "validator": {"type": "spark_username_null_empty"},
        "transformation": {"type": "spark_upper_username"},
        "sink": {"type": "parquet", "options": {"path": str(output_path)}},
    }

    builder = PipelineBuilder()
    execusion = builder.build(config)

    execusion.run()

    assert output_path.exists()
