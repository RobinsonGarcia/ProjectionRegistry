from typing import Any, Tuple
from ..base.grid import BaseGridGeneration
from .config import GnomonicConfig
from ..exceptions import GridGenerationError
import numpy as np
import logging

logger = logging.getLogger('gnomonic_projection.gnomonic.grid')

class GnomonicGridGeneration(BaseGridGeneration):
    """
    Grid generation for Gnomonic projection.

    This class handles the creation of forward and backward grids necessary for
    performing Gnomonic projections. The grid generation is based on the projection's
    field of view and the spherical trigonometry principles outlined in the mathematical
    foundation of the Gnomonic projection.

    ## Projection Processes:

    1. **Forward Projection:**
       
       The forward grid is generated based on the field of view (`fov_deg`) and the radius
       of the sphere (`R`). It creates a meshgrid of points on the Gnomonic projection plane
       where each point corresponds to a specific geographic coordinate in the equirectangular
       (input) image. This grid facilitates the mapping of the input image onto the projection plane.

    2. **Backward Projection:**
       
       The backward grid spans the entire range of longitude and latitude defined by
       `lon_min`, `lon_max`, `lat_min`, and `lat_max`. This grid is used to map points from
       the Gnomonic projection plane back to the equirectangular (output) image. Essentially,
       it enables the reverse transformation, allowing the projection to be undone or
       converted back to the standard equirectangular format.
    """

    def __init__(self, config: GnomonicConfig) -> None:
        """
        Initialize the GnomonicGridGeneration with the given configuration.

        Args:
            config (GnomonicConfig): The configuration object containing projection parameters.

        Raises:
            TypeError: If the config is not an instance of GnomonicConfig.
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
        Create a grid based on the specified direction.

        Args:
            direction (str): Direction of grid creation ('forward' or 'backward').

        Returns:
            Tuple[np.ndarray, np.ndarray]: Generated grid arrays.
                - For 'forward': Returns planar X and Y coordinates on the Gnomonic projection plane.
                - For 'backward': Returns longitude and latitude grids spanning the full geographic range.

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

                logger.debug(f"Generated x_vals and y_vals for forward grid.")

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

                logger.debug(f"Generated lon_vals and lat_vals for backward grid.")

                # Create meshgrid for geographic coordinates (longitude and latitude)
                grid_lon, grid_lat = np.meshgrid(lon_vals, lat_vals)
                logger.debug("Backward grid created successfully spanning full geographic range.")
                return grid_lon, grid_lat
            except Exception as e:
                error_msg = f"Failed to create backward grid: {e}"
                logger.exception(error_msg)
                raise GridGenerationError(error_msg) from e
        else:
            error_msg = "Direction must be 'forward' or 'backward'."
            logger.error(error_msg)
            raise GridGenerationError(error_msg)