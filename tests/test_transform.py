import pytest
from projection.base.transform import CoordinateTransformer
from projection.gnomonic.config import GnomonicConfig
from projection.exceptions import TransformationError, ConfigurationError
import numpy as np

def test_latlon_to_image_coords_valid():
    config = GnomonicConfig()
    lat = np.array([[0, 45], [90, -45]])
    lon = np.array([[-180, 0], [180, 90]])
    shape = (180, 360, 3)  # Example equirectangular image shape
    map_x, map_y = CoordinateTransformer.latlon_to_image_coords(lat, lon, config, shape)
    assert map_x.shape == lat.shape
    assert map_y.shape == lat.shape

def test_latlon_to_image_coords_invalid_inputs():
    config = GnomonicConfig()
    # First call: Invalid latitude input, but include all required parameters
    with pytest.raises(TransformationError):
        CoordinateTransformer.latlon_to_image_coords("lat", np.array([0]), config, (100, 100))
    
    # Second call: Missing 'lon_min' attribute
    with pytest.raises(ConfigurationError):
        config_invalid = GnomonicConfig()
        del config_invalid.lon_min  # Remove required attribute
        CoordinateTransformer.latlon_to_image_coords(np.array([0]), np.array([0]), config_invalid, (100, 100))

def test_xy_to_image_coords_valid():
    config = GnomonicConfig()
    x = np.array([[0, 1], [2, 3]])
    y = np.array([[4, 5], [6, 7]])
    map_x, map_y = CoordinateTransformer.xy_to_image_coords(x, y, config)
    assert map_x.shape == x.shape
    assert map_y.shape == y.shape

def test_xy_to_image_coords_invalid_inputs():
    config = GnomonicConfig()
    with pytest.raises(TransformationError):
        CoordinateTransformer.xy_to_image_coords("x", np.array([0]), config)
    with pytest.raises(ConfigurationError):
        config_invalid = GnomonicConfig()
        del config_invalid.x_min  # Remove required attribute
        CoordinateTransformer.xy_to_image_coords(np.array([0]), np.array([0]), config_invalid)

def test_xy_to_image_coords_invalid_shape():
    config = GnomonicConfig()
    x = np.array([0,1,2])
    y = np.array([3,4,5])
    with pytest.raises(TransformationError):
        CoordinateTransformer.latlon_to_image_coords(np.array([0,1,2]), np.array([3,4,5]), config, (100,))

def test_latlon_to_image_coords_computation():
    config = GnomonicConfig(
        lon_min=0,
        lon_max=360,
        lat_min=-90,
        lat_max=90
    )
    lat = np.array([[0, 90], [-90, 45]])
    lon = np.array([[0, 180], [360, 90]])
    shape = (180, 360, 3)
    map_x, map_y = CoordinateTransformer.latlon_to_image_coords(lat, lon, config, shape)
    expected_map_x = (lon - config.lon_min) / (config.lon_max - config.lon_min) * (shape[1] - 1)
    expected_map_y = (config.lat_max - lat) / (config.lat_max - config.lat_min) * (shape[0] - 1)
    assert np.allclose(map_x, expected_map_x)
    assert np.allclose(map_y, expected_map_y)