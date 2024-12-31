# /Users/robinsongarcia/projects/gnomonic/tests/conftest.py

# Standard library imports
from unittest.mock import Mock

# Third-party imports
import pytest

# Local imports
from projection.gnomonic.config import GnomonicConfig
from projection.base.config import BaseProjectionConfig
from projection.processor import ProjectionProcessor

@pytest.fixture
def mock_grid_generation():
    """
    Fixture to provide a mock grid generation object with a create_grid method.
    """
    mock = Mock()
    mock.create_grid.return_value = (Mock(), Mock())  # Mocked grid arrays
    return mock

@pytest.fixture
def projection_processor(mock_grid_generation):
    """
    Fixture to provide a ProjectionProcessor with mocked components.
    """
    config = GnomonicConfig()
    base_config = BaseProjectionConfig(config)
    base_config.create_projection = Mock()  # Mock create_projection to avoid NotImplementedError
    base_config.create_grid_generation = Mock(return_value=mock_grid_generation)
    processor = ProjectionProcessor(base_config)
    return processor