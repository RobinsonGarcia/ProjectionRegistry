# projection/stereographic/grid.py

import logging
import numpy as np
from typing import Tuple
from ..base.grid import BaseGridGeneration
from .config import StereographicConfig
from ..exceptions import GridGenerationError

logger = logging.getLogger("projection.stereographic.grid")


class StereographicGridGeneration(BaseGridGeneration):
    """
    Generates forward and backward grids for Stereographic projection.
    """

    def projection_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create the planar (X, Y) grid for forward projection.
        """
        logger.debug("Generating Stereographic forward grid.")
        try:
            R = self.config.R * self.config.scaling_factor
            # Define the extent based on field of view or bounding box
            max_extent = 2 * R * np.tan(np.deg2rad(90))  # Typically covers the hemisphere
            x_vals = np.linspace(-max_extent, max_extent, self.config.x_points)
            y_vals = np.linspace(-max_extent, max_extent, self.config.y_points)
            grid_x, grid_y = np.meshgrid(x_vals, y_vals)
            logger.debug(f"Generated projection grid with shape {grid_x.shape}.")
            return grid_x, grid_y
        except Exception as e:
            error_msg = f"Failed to generate forward grid: {e}"
            logger.exception(error_msg)
            raise GridGenerationError(error_msg)

    def spherical_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create the (lon, lat) grid for backward projection.
        """
        logger.debug("Generating Stereographic spherical grid.")
        try:
            lon_vals = np.linspace(self.config.lon_min, self.config.lon_max, self.config.lon_points)
            lat_vals = np.linspace(self.config.lat_min, self.config.lat_max, self.config.lat_points)
            grid_lon, grid_lat = np.meshgrid(lon_vals, lat_vals)
            logger.debug(f"Generated spherical grid with shape {grid_lon.shape}.")
            return grid_lon, grid_lat
        except Exception as e:
            error_msg = f"Failed to generate spherical grid: {e}"
            logger.exception(error_msg)
            raise GridGenerationError(error_msg)