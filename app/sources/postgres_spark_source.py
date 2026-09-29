from pyspark.sql import DataFrame
from .source_base import Source


class PostgresSparkSource(Source[DataFrame]):
    def __init__(host: str, port: int, database: str, table: str):
        ...