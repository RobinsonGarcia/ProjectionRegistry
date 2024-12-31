from ..base.grid import BaseGridGeneration
import numpy as np
import logging

logger = logging.getLogger('projection.mercator.grid')

class MercatorGridGeneration(BaseGridGeneration):
    """
    Grid generation for Mercator projection.
    """

    def __init__(self, config):
        self.config = config

    def _create_grid(self, direction: str):
        if direction == 'forward':
            lon = np.linspace(
                self.config.config.lon_min, self.config.config.lon_max, self.config.config.x_points
            )
            lat = np.linspace(
                self.config.config.lat_min, self.config.config.lat_max, self.config.config.y_points
            )
            grid_lon, grid_lat = np.meshgrid(lon, lat)
            return grid_lon, grid_lat
        elif direction == 'backward':
            x = np.linspace(-1, 1, self.config.config.x_points)
            y = np.linspace(-1, 1, self.config.config.y_points)
            return np.meshgrid(x, y)
        else:
            raise ValueError("Invalid direction. Must be 'forward' or 'backward'.")