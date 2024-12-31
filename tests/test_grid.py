import pytest
from projection.base.grid import BaseGridGeneration
from projection.gnomonic.grid import GnomonicGridGeneration
from projection.gnomonic.config import GnomonicConfig
from projection.exceptions import GridGenerationError, ConfigurationError
import numpy as np

class MockGridGeneration(BaseGridGeneration):
    def _create_grid(self, direction: str):
        return np.zeros((10, 10)), np.zeros((10, 10))

def test_base_grid_generation_invalid_direction():
    base_grid = BaseGridGeneration()
    with pytest.raises(GridGenerationError) as exc_info:
        base_grid.create_grid('invalid_direction')
    assert "Direction must be 'forward' or 'backward'." in str(exc_info.value)

def test_base_grid_generation_not_implemented():
    base_grid = BaseGridGeneration()
    with pytest.raises(GridGenerationError) as exc_info:
        base_grid.create_grid('forward')  # Should call _create_grid and raise
    assert "Subclasses must implement create_grid." in str(exc_info.value)

def test_gnomonic_grid_generation_forward():
    config = GnomonicConfig()
    grid_gen = GnomonicGridGeneration(config)
    x_grid, y_grid = grid_gen.create_grid('forward')
    assert x_grid.shape == (config.y_points, config.x_points)
    assert y_grid.shape == (config.y_points, config.x_points)
    assert np.all(x_grid >= config.x_min) and np.all(x_grid <= config.x_max)
    assert np.all(y_grid >= config.y_min) and np.all(y_grid <= config.y_max)

def test_gnomonic_grid_generation_backward():
    config = GnomonicConfig()
    grid_gen = GnomonicGridGeneration(config)
    lon_grid, lat_grid = grid_gen.create_grid('backward')
    assert lon_grid.shape == (config.lat_points, config.lon_points)
    assert lat_grid.shape == (config.lat_points, config.lon_points)
    assert np.all(lon_grid >= config.lon_min) and np.all(lon_grid <= config.lon_max)
    assert np.all(lat_grid >= config.lat_min) and np.all(lat_grid <= config.lat_max)

def test_gnomonic_grid_generation_invalid_direction():
    config = GnomonicConfig()
    grid_gen = GnomonicGridGeneration(config)
    with pytest.raises(GridGenerationError) as exc_info:
        grid_gen.create_grid('invalid')
    assert "Direction must be 'forward' or 'backward'." in str(exc_info.value)