from unittest.mock import Mock, patch

from app.engines.engine import main


@patch("app.engines.engine.PipelineBuilder")
@patch("app.engines.engine.load_pipeline_configs")
def test_engine(mock_load_config, mock_pipeline_builder):
    config = {"name": "test_pipeline"}
    fake_execution = Mock()

    mock_load_config.return_value = [config]
    builder_instance = mock_pipeline_builder.return_value
    builder_instance.build.return_value = fake_execution

    main()

    mock_load_config.assert_called_once()
    builder_instance.build.assert_called_once_with(config)
    fake_execution.run.assert_called_once()
