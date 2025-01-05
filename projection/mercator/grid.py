from ..base.grid import BaseGridGeneration
import numpy as np
import logging

logger = logging.getLogger('projection.mercator.grid')

class MercatorGridGeneration(BaseGridGeneration):
    """
    Grid generation for Mercator projection.
    """
    

    def projection_grid(self):     
        y_max = np.log(np.tan(np.pi / 4 + np.radians(self.config.config.lat_max) / 2))
        y_min = np.log(np.tan(np.pi / 4 + np.radians(self.config.config.lat_min) / 2))
        lat = np.linspace(y_min,y_max ,self.config.config.y_points)
        lon = np.linspace(self.config.config.lon_min, self.config.config.lon_max, self.config.config.x_points)
        lon = np.radians(lon)
        grid_lon, grid_lat = np.meshgrid(lon, lat)
        return grid_lon, grid_lat
    def spherical_grid(self):
        x = np.linspace(self.config.config.lon_min, self.config.config.lon_max, self.config.config.x_points)
        y = np.linspace(self.config.config.lat_max, self.config.config.lat_min, self.config.config.y_points)
        map_y, map_x =  np.meshgrid(x, y)
        return map_x, map_y
