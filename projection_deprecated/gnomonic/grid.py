from ..base.grid import BaseGridGeneration
from .config import GnomonicConfig
import numpy as np

class GnomonicGridGeneration(BaseGridGeneration):
    def __init__(self, config: GnomonicConfig):
        self.config = config

    def create_grid(self, direction):
        if direction == 'forward':
            x_vals = np.linspace(self.config.x_min, self.config.x_max, self.config.x_points)
            y_vals = np.linspace(self.config.y_min, self.config.y_max, self.config.y_points)
            return np.meshgrid(x_vals, y_vals)
        elif direction == 'backward':
            lon_vals = np.linspace(self.config.lon_min, self.config.lon_max, self.config.lon_points)
            lat_vals = np.linspace(self.config.lat_min, self.config.lat_max, self.config.lat_points)
            return np.meshgrid(lon_vals, lat_vals)
        else:
            raise ValueError("Direction must be 'forward' or 'backward'.")