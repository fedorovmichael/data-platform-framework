import os


def test_spark_write_read_minio(spark):
    hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

    hadoop_conf.set("fs.s3a.endpoint", os.environ["MINIO_ENDPOINT"])
    hadoop_conf.set("fs.s3a.access.key", os.environ["MINIO_ACCESS_KEY"])
    hadoop_conf.set("fs.s3a.secret.key", os.environ["MINIO_SECRET_KEY"])
    hadoop_conf.set("fs.s3a.path.style.access", "true")
    hadoop_conf.set("fs.s3a.connection.ssl.enabled", "false")
    hadoop_conf.set(
        "fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    )

    # 2. Create a DataFrame
    df = spark.createDataFrame(
        [
            (1, "Alice"),
            (2, "Bob"),
            (3, "Charlie"),
        ],
        ["id", "username"],
    )

    # 3. Write Parquet to MinIO
    path = "s3a://data-platform/integration-test/users/"

    df.write.mode("overwrite").parquet(path)

    # 4. Read Parquet from MinIO
    result = spark.read.parquet(path)

    # 5. Verify
    user_names = [
        "Alice",
        "Bob",
        "Charlie",
    ]

    assert result.count() == 3
    assert sorted(row.username for row in result.collect()) == user_names
