import pytest
from projection.base.config import BaseProjectionConfig, BaseProjectionConfigModel
from projection.gnomonic.config import GnomonicConfig
from projection.exceptions import ConfigurationError
import cv2

def test_base_projection_config_valid():
    gnomonic_config = GnomonicConfig()
    base_config = BaseProjectionConfig(gnomonic_config)
    assert isinstance(base_config.params, BaseProjectionConfigModel), "BaseProjectionConfigModel not initialized correctly"

def test_base_projection_config_invalid():
    with pytest.raises(ConfigurationError) as exc_info:
        BaseProjectionConfig(config_object={})  # Missing 'config' attribute
    assert "Configuration object must have a 'config' attribute." in str(exc_info.value)

def test_gnomonic_config_valid():
    config = GnomonicConfig(
        R=1,
        phi1_deg=0,
        lam0_deg=0,
        fov_deg=90,
        x_points=1024,
        y_points=1024,
        lon_points=2048,
        lat_points=1024,
        x_min=-1,
        x_max=1,
        y_min=-1,
        y_max=1,
        lon_min=-180,
        lon_max=180,
        lat_min=-90,
        lat_max=90,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0
    )
    assert config.R == 1
    assert config.fov_deg == 90

def test_gnomonic_config_invalid_fov():
    with pytest.raises(ConfigurationError) as exc_info:
        GnomonicConfig(fov_deg=200)  # Invalid fov_deg
    assert "Field of view (fov_deg) must be between 0 and 180 degrees." in str(exc_info.value)

def test_gnomonic_config_update():
    config = GnomonicConfig(fov_deg=90)
    config.update(fov_deg=120)
    assert config.fov_deg == 120
    with pytest.raises(ConfigurationError) as exc_info:
        config.update(fov_deg=-10)  # Invalid update
    assert "Field of view (fov_deg) must be between 0 and 180 degrees." in str(exc_info.value)