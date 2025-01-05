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

    def from_projection_to_spherical(self, lon: np.ndarray, lat: np.ndarray):
        lon = lon / self.config.R
        lat =  np.pi / 2 - 2 * np.arctan(np.e**(lat/ self.config.R))
        logger.debug("Mercator forward projection computed successfully.")
        return lat, lon # (lat,lon)


    def from_spherical_to_projection(self, x: np.ndarray, y: np.ndarray):
        lon_rad = np.radians(x)
        lat_rad = np.radians(y)#_clamped)
        x = 1 * lon_rad
        y = 1 * np.log(np.tan(np.pi / 4 + lat_rad / 2))
        mask = np.ones_like(x) == 1
        return x, y, mask

