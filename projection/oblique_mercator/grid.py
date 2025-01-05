# projection/oblique_mercator/grid.py
import numpy as np
import logging
from typing import Tuple
from ..base.grid import BaseGridGeneration

logger = logging.getLogger("projection.oblique_mercator.grid")

class ObliqueMercatorGridGeneration(BaseGridGeneration):
    """
    Generates the forward (x, y) grid and the backward (lon, lat) grid.
    """

    def projection_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Produce (x_grid, y_grid) for the forward projection.
        We treat fov_deg to define the maximum extent in x,y (similar to Gnomonic).
        """
        half_fov_rad = np.deg2rad(self.config.fov_deg / 2.0)
        x_extent = np.tan(half_fov_rad) * self.config.R
        y_extent = np.tan(half_fov_rad) * self.config.R

        x_vals = np.linspace(-x_extent, x_extent, self.config.x_points)
        y_vals = np.linspace(-y_extent, y_extent, self.config.y_points)
        grid_x, grid_y = np.meshgrid(x_vals, y_vals)
        return grid_x, grid_y

    def spherical_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Produce (lon_grid, lat_grid) for the backward projection.
        """
        lon_vals = np.linspace(self.config.lon_min, self.config.lon_max, self.config.x_points)
        lat_vals = np.linspace(self.config.lat_min, self.config.lat_max, self.config.y_points)
        grid_lon, grid_lat = np.meshgrid(lon_vals, lat_vals)
        return grid_lon, grid_lat