import pytest
from py4j.protocol import Py4JJavaError


def test_postgres_spark_sink_integration_append_mode(
    spark, postgres_test_table, postgres_sink
):

    df = spark.createDataFrame(
        [
            (3, "Charlie", "charlie@example.com"),
        ],
        ["id", "username", "email"],
    )

    _, conn = postgres_test_table
    sink = postgres_sink()
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


def test_postgres_spark_sink_integration_overwrite_mode(
    spark, postgres_test_table, postgres_sink
):

    df = spark.createDataFrame(
        [(3, "Charlie", "charlie@example.com")],
        ["id", "username", "email"],
    )

    _, conn = postgres_test_table

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.table_constraints
            WHERE table_schema = 'public'
            AND table_name = 'integration_test_users'
            AND constraint_type = 'PRIMARY KEY'
        """)

        assert cursor.fetchone()[0] == 1

    sink = postgres_sink(mode="overwrite")
    sink.write(df)

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, username, email 
            FROM integration_test_users
            ORDER BY id;
        """)

        rows = cursor.fetchall()
        assert rows == [(3, "Charlie", "charlie@example.com")]

        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.table_constraints
            WHERE table_name = 'integration_test_users'
            AND constraint_type = 'PRIMARY KEY'
            AND table_schema = 'public' 
        """)

        primary_key_count = cursor.fetchone()[0]
        assert primary_key_count == 0


def test_postgres_spark_sink_integration_duplicate_primary_key(
    spark, postgres_test_table, postgres_sink
):

    df = spark.createDataFrame(
        [(1, "Alice", "alice@example.com")],
        ["id", "username", "email"],
    )

    _, conn = postgres_test_table
    sink = postgres_sink()

    with pytest.raises(Py4JJavaError, match="duplicate key"):
        sink.write(df)

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, username
            FROM integration_test_users
            ORDER BY id
        """)

        rows = cursor.fetchall()
        assert rows == [(1, "Alice"), (2, "Bob")]
