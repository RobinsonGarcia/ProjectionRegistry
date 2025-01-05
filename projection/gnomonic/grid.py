from typing import Any, Tuple
from ..base.grid import BaseGridGeneration
from .config import GnomonicConfig
from ..exceptions import GridGenerationError
import numpy as np
import logging

logger = logging.getLogger('gnomonic_projection.gnomonic.grid')

class GnomonicGridGeneration(BaseGridGeneration):
    
    def projection_grid(self):
        half_fov_rad = np.deg2rad(self.config.fov_deg / 2)
        x_max = np.tan(half_fov_rad) * self.config.R
        y_max = np.tan(half_fov_rad) * self.config.R
        x_vals = np.linspace(-x_max, x_max, self.config.x_points)
        y_vals = np.linspace(-y_max, y_max, self.config.y_points)
        grid_x, grid_y = np.meshgrid(x_vals, y_vals)
        return grid_x, grid_y       
    
    def spherical_grid(self):
        # Generate linearly spaced points for longitude and latitude spanning the full geographic range
        lon_vals = np.linspace(self.config.lon_min, self.config.lon_max, self.config.lon_points)
        lat_vals = np.linspace(self.config.lat_min, self.config.lat_max, self.config.lat_points)
        grid_lon, grid_lat = np.meshgrid(lon_vals, lat_vals)
        return grid_lon, grid_lat        
    