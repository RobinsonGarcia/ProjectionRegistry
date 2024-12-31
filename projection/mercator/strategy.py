from ..base.strategy import BaseProjectionStrategy
import numpy as np
import logging

logger = logging.getLogger('projection.mercator.strategy')

class MercatorProjectionStrategy(BaseProjectionStrategy):
    """
    Projection strategy for Mercator projection.
    """

    def __init__(self, config):
        self.config = config

    def forward(self, lon: np.ndarray, lat: np.ndarray):
        """
        Convert geographic coordinates to Cartesian coordinates.
        """
        x = self.config.config.R * np.radians(lon)
        y = self.config.config.R * np.log(np.tan(np.pi / 4 + np.radians(lat) / 2))
        return x, y

    def backward(self, x: np.ndarray, y: np.ndarray):
        """
        Convert Cartesian coordinates to geographic coordinates.
        """
        lon = np.degrees(x / self.config.config.R)
        lat = np.degrees(2 * np.arctan(np.exp(y / self.config.config.R)) - np.pi / 2)
        mask = (lon >= self.config.config.lon_min) & (lon <= self.config.config.lon_max) & \
               (lat >= self.config.config.lat_min) & (lat <= self.config.config.lat_max)
        return lon, lat, mask