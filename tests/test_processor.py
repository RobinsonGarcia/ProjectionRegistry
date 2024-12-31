import pytest
from unittest.mock import Mock
from projection.processor import ProjectionProcessor
from projection.base.config import BaseProjectionConfig
from projection.exceptions import ProcessingError, GridGenerationError, InterpolationError
from projection.gnomonic.config import GnomonicConfig
import numpy as np

def test_processor_initialization():
    config = GnomonicConfig()
    base_config = BaseProjectionConfig(config)
    base_config.create_projection = Mock()  # Mock to avoid NotImplementedError
    base_config.create_grid_generation = Mock()
    processor = ProjectionProcessor(base_config)
    assert isinstance(processor, ProjectionProcessor)

def test_processor_forward_invalid_image():
    config = GnomonicConfig()
    base_config = BaseProjectionConfig(config)
    base_config.create_projection = Mock()
    base_config.create_grid_generation = Mock()
    processor = ProjectionProcessor(base_config)
    with pytest.raises(ValueError):
        processor.forward("not_an_image")