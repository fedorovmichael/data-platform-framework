import psycopg
import os

from app.sources.postgres_spark_source import PostgresCredentials
from app.sinks.sink_postgres import SinkSparkPostgres


def test_postgres_spark_sink_integration(spark):

    _host = os.environ["POSTGRES_TEST_HOST"]
    _port = int(os.getenv("POSTGRES_TEST_PORT", "5432"))
    _dbname = os.environ["POSTGRES_TEST_DB"]
    _user = os.environ["POSTGRES_TEST_USER"]
    _password = os.environ["POSTGRES_TEST_PASSWORD"]

    df = spark.createDataFrame(
        [
            (1, "Alice", "alice@example.com"),
            (2, "Bob", "bob@example.com"),
            (3, "Charlie", "charlie@example.com"),
        ],
        ["id", "username", "email"],
    )

    credentials = PostgresCredentials(_user, _password)
    sink = SinkSparkPostgres(
        host=_host,
        port=_port,
        database=_dbname,
        table="integration_test_users",
        credentials=credentials,
    )


    conn = psycopg.connect(
        host=_host,
        port=_port,
        dbname=_dbname,
        user=_user,
        password=_password,
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE integration_test_users (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(100),
                    email VARCHAR(255)
                )
            """)

            conn.commit()

            sink.write(df)

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, email 
                FROM integration_test_users
                ORDER BY id;
            """)

            rows = cursor.fetchall()

            assert rows == [
                (1, "Alice", "alice@example.com"),
                (2, "Bob", "bob@example.com"),
                (3, "Charlie", "charlie@example.com"),
            ]
    finally:
        conn.rollback()
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS integration_test_users")

        conn.commit()
        conn.close()
