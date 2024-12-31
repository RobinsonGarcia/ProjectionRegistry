# tests/test_strategy.py

import pytest
from projection.base.strategy import BaseProjectionStrategy
from projection.gnomonic.strategy import GnomonicProjectionStrategy
from projection.gnomonic.config import GnomonicConfig
from projection.exceptions import ProcessingError
import numpy as np

class MockProjectionStrategy(BaseProjectionStrategy):
    def forward(self, x: np.ndarray, y: np.ndarray):
        return np.zeros_like(x), np.zeros_like(y)
    
    def backward(self, lat: np.ndarray, lon: np.ndarray):
        return np.zeros_like(lat), np.zeros_like(lon), np.ones_like(lat)

def test_base_projection_strategy_forward_not_implemented():
    base_strategy = BaseProjectionStrategy()
    with pytest.raises(ProcessingError) as exc_info:
        base_strategy.forward(np.array([1,2]), np.array([3,4]))
    assert "x and y must be NumPy ndarrays." not in str(exc_info.value)
    assert "Subclasses must implement forward." in str(exc_info.value)

def test_base_projection_strategy_backward_not_implemented():
    base_strategy = BaseProjectionStrategy()
    with pytest.raises(ProcessingError) as exc_info:
        base_strategy.backward(np.array([1,2]), np.array([3,4]))
    assert "lat and lon must be NumPy ndarrays." not in str(exc_info.value)
    assert "Subclasses must implement backward." in str(exc_info.value)

def test_gnomonic_projection_strategy_forward():
    config = GnomonicConfig()
    strategy = GnomonicProjectionStrategy(config)
    x = np.array([[0,1], [2,3]])
    y = np.array([[4,5], [6,7]])
    lat, lon = strategy.forward(x, y)
    assert lat.shape == x.shape
    assert lon.shape == y.shape

def test_gnomonic_projection_strategy_backward():
    config = GnomonicConfig()
    strategy = GnomonicProjectionStrategy(config)
    lat = np.array([[0,45], [90,135]])
    lon = np.array([[-180, -90], [0, 90]])
    x, y, mask = strategy.backward(lat, lon)
    assert x.shape == lat.shape
    assert y.shape == lon.shape
    assert mask.shape == lat.shape
    assert np.all(mask == True)  # Based on GnomonicConfig defaults

def test_gnomonic_projection_strategy_invalid_inputs():
    config = GnomonicConfig()
    strategy = GnomonicProjectionStrategy(config)
    with pytest.raises(ProcessingError):
        strategy.forward([1,2], np.array([3,4]))  # x is not np.ndarray
    with pytest.raises(ProcessingError):
        strategy.backward(np.array([1,2]), "invalid_lon")  # lon is not np.ndarray