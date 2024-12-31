### /Users/robinsongarcia/projects/gnomonic/projection/gnomonic/grid.py ###

from typing import Any, Tuple
from ..base.grid import BaseGridGeneration
from .config import GnomonicConfig
from ..exceptions import GridGenerationError, ConfigurationError
import numpy as np
import logging

# Initialize logger for this module
logger = logging.getLogger('gnomonic_projection.gnomonic.grid')

class GnomonicGridGeneration(BaseGridGeneration):
    """
    Grid generation implementation for Gnomonic projections.
    """
    def __init__(self, config: GnomonicConfig) -> None:
        """
        Initialize the grid generation with the provided configuration.

        Args:
            config (GnomonicConfig): The Gnomonic projection configuration.

        Raises:
            TypeError: If 'config' is not an instance of GnomonicConfig.
        """
        logger.debug("Initializing GnomonicGridGeneration.")
        if not isinstance(config, GnomonicConfig):
            error_msg = f"config must be an instance of GnomonicConfig, got {type(config)} instead."
            logger.error(error_msg)
            raise TypeError(error_msg)
        self.config: GnomonicConfig = config
        logger.info("GnomonicGridGeneration initialized successfully.")

    def _create_grid(self, direction: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Internal method to create a grid based on the specified direction.

        Args:
            direction (str): Direction of grid creation ('forward' or 'backward').

        Returns:
            Tuple[np.ndarray, np.ndarray]: Generated grid arrays.

        Raises:
            GridGenerationError: If grid creation fails.
        """
        logger.debug(f"GnomonicGridGeneration: Creating '{direction}' grid.")
        if direction == 'forward':
            try:
                x_vals = np.linspace(self.config.x_min, self.config.x_max, self.config.x_points)
                y_vals = np.linspace(self.config.y_min, self.config.y_max, self.config.y_points)
                grid_x, grid_y = np.meshgrid(x_vals, y_vals)
                logger.debug("Forward grid created successfully.")
                return grid_x, grid_y
            except Exception as e:
                error_msg = f"Failed to create forward grid: {e}"
                logger.exception(error_msg)
                raise GridGenerationError(error_msg) from e
        elif direction == 'backward':
            try:
                lon_vals = np.linspace(self.config.lon_min, self.config.lon_max, self.config.lon_points)
                lat_vals = np.linspace(self.config.lat_min, self.config.lat_max, self.config.lat_points)
                grid_lon, grid_lat = np.meshgrid(lon_vals, lat_vals)
                logger.debug("Backward grid created successfully.")
                return grid_lon, grid_lat
            except Exception as e:
                error_msg = f"Failed to create backward grid: {e}"
                logger.exception(error_msg)
                raise GridGenerationError(error_msg) from e
        else:
            error_msg = "Direction must be 'forward' or 'backward'."
            logger.error(error_msg)
            raise GridGenerationError(error_msg)