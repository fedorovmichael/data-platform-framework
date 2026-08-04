import pytest
from app.sinks.sink_parquet import SinkParquet


@pytest.mark.parametrize("path", ["", " ", None, 123, [], {}])
def test_sink_path_must_be_non_empty(path):

    with pytest.raises(
        ValueError, match="Parquet output path must be a non-empty string."
    ):
        SinkParquet(path=path)
