import pytest
from unittest.mock import Mock
from projection.processor import ProjectionProcessor
from projection.gnomonic.config import GnomonicConfig
from projection.base.config import BaseProjectionConfig
from projection.exceptions import ProcessingError, GridGenerationError
import numpy as np

def test_backward_projection_pipeline():
    config = GnomonicConfig()
    base_config = BaseProjectionConfig(config)
    base_config.create_projection = Mock()  # Mock create_projection to avoid NotImplementedError
    
    # Create a mock for grid generation with a create_grid method
    mock_grid_generation = Mock()
    mock_grid_generation.create_grid.return_value = (np.zeros((2, 2)), np.zeros((2, 2)))
    base_config.create_grid_generation = Mock(return_value=mock_grid_generation)
    
    processor = ProjectionProcessor(base_config)

    rect_img = np.ones((2, 2, 3), dtype=np.uint8) * 255
    back_projected_img = processor.backward(rect_img)
    assert back_projected_img.shape == rect_img.shape
    assert not np.all(back_projected_img == 0)