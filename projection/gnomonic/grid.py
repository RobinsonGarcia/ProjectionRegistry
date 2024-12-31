from typing import Any, Tuple
from ..base.grid import BaseGridGeneration
from .config import GnomonicConfig
from ..exceptions import GridGenerationError
import numpy as np
import logging

logger = logging.getLogger('gnomonic_projection.gnomonic.grid')

class GnomonicGridGeneration(BaseGridGeneration):
    def __init__(self, config: GnomonicConfig) -> None:
        logger.debug("Initializing GnomonicGridGeneration.")
        if not isinstance(config, GnomonicConfig):
            error_msg = f"config must be an instance of GnomonicConfig, got {type(config)} instead."
            logger.error(error_msg)
            raise TypeError(error_msg)
        self.config: GnomonicConfig = config
        logger.info("GnomonicGridGeneration initialized successfully.")

    def _create_grid(self, direction: str) -> Tuple[np.ndarray, np.ndarray]:
        logger.debug(f"GnomonicGridGeneration: Creating '{direction}' grid.")
        if direction == 'forward':
            try:
                half_fov_rad = np.deg2rad(self.config.fov_deg / 2)
                x_max = np.tan(half_fov_rad) * self.config.R
                y_max = np.tan(half_fov_rad) * self.config.R
                x_vals = np.linspace(-x_max, x_max, self.config.x_points)
                y_vals = np.linspace(-y_max, y_max, self.config.y_points)
                grid_x, grid_y = np.meshgrid(x_vals, y_vals)
                logger.debug("Forward grid created successfully with dynamic FOV.")
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