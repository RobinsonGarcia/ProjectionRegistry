from typing import Any, Tuple
from ..base.grid import BaseGridGeneration
from .config import GnomonicConfig
from ..exceptions import GridGenerationError
import numpy as np
import logging

logger = logging.getLogger('gnomonic_projection.gnomonic.grid')

class GnomonicGridGeneration(BaseGridGeneration):
    """
    Grid Generation for Gnomonic Projection.

    This class is responsible for creating the necessary grids for both forward (equirectangular to Gnomonic)
    and inverse (Gnomonic to equirectangular) projections. It leverages the projection's field of view
    and spherical trigonometry principles to ensure accurate mapping between geographic and planar coordinates.

    ## Projection Processes:

    1. **Forward Transformation (Equirectangular to Gnomonic):**

       - **Field of View Consideration:** Generates a meshgrid on the Gnomonic projection plane based on the specified
         field of view (`fov_deg`) and the Earth's radius (`R`).
       - **Grid Points:** Creates a grid of `x_points` and `y_points` to represent the resolution of the projection plane.

    2. **Inverse Transformation (Gnomonic to Equirectangular):**

       - **Geographic Coverage:** Generates a meshgrid covering the full range of longitude and latitude defined by
         `lon_min`, `lon_max`, `lat_min`, and `lat_max`.
       - **Grid Points:** Utilizes `lon_points` and `lat_points` to define the resolution of the equirectangular grid.
    """

    def __init__(self, config) -> None:
        """
        Initialize the GnomonicGridGeneration with the given configuration.

        Args:
            config (GnomonicConfig): The configuration object containing projection parameters.

        Raises:
            TypeError: If the config is not an instance of GnomonicConfig.
        """
        logger.debug("Initializing GnomonicGridGeneration.")

        self.config = config
        logger.info("GnomonicGridGeneration initialized successfully.")

    def _create_grid(self, direction: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create a grid based on the specified transformation direction.

        Args:
            direction (str): Direction of grid creation ('forward' for Equirectangular to Gnomonic
                             or 'inverse' for Gnomonic to Equirectangular).

        Returns:
            Tuple[np.ndarray, np.ndarray]: Generated grid arrays.
                - For 'forward': Returns planar X and Y coordinates on the Gnomonic projection plane.
                - For 'inverse': Returns longitude and latitude grids spanning the full geographic range.

        Raises:
            GridGenerationError: If grid creation fails due to invalid parameters or internal errors.
        """
        logger.debug(f"GnomonicGridGeneration: Creating '{direction}' grid.")
        if direction == 'forward':
            try:
                # Calculate maximum extents based on field of view
                half_fov_rad = np.deg2rad(self.config.fov_deg / 2)
                x_max = np.tan(half_fov_rad) * self.config.R
                y_max = np.tan(half_fov_rad) * self.config.R

                logger.debug(f"Computed x_max: {x_max}, y_max: {y_max} based on fov_deg: {self.config.fov_deg} and R: {self.config.R}")

                # Generate linearly spaced points in x and y directions
                x_vals = np.linspace(-x_max, x_max, self.config.x_points)
                y_vals = np.linspace(-y_max, y_max, self.config.y_points)

                logger.debug("Generated x_vals and y_vals for forward grid.")

                # Create meshgrid for planar coordinates on the Gnomonic projection plane
                grid_x, grid_y = np.meshgrid(x_vals, y_vals)
                logger.debug("Forward grid created successfully with dynamic FOV.")
                return grid_x, grid_y
            except Exception as e:
                error_msg = f"Failed to create forward grid: {e}"
                logger.exception(error_msg)
                raise GridGenerationError(error_msg) from e
        elif direction == 'backward':
            try:
                # Generate linearly spaced points for longitude and latitude spanning the full geographic range
                lon_vals = np.linspace(self.config.lon_min, self.config.lon_max, self.config.lon_points)
                lat_vals = np.linspace(self.config.lat_min, self.config.lat_max, self.config.lat_points)

                logger.debug("Generated lon_vals and lat_vals for inverse grid.")

                # Create meshgrid for geographic coordinates (longitude and latitude)
                grid_lon, grid_lat = np.meshgrid(lon_vals, lat_vals)
                logger.debug("Inverse grid created successfully spanning full geographic range.")
                return grid_lon, grid_lat
            except Exception as e:
                error_msg = f"Failed to create inverse grid: {e}"
                logger.exception(error_msg)
                raise GridGenerationError(error_msg) from e
        else:
            error_msg = "Direction must be 'forward' or 'backward'."
            logger.error(error_msg)
            raise GridGenerationError(error_msg)