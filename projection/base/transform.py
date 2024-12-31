from typing import Any, Tuple
import numpy as np
import logging
from ..exceptions import TransformationError, ConfigurationError

# Initialize logger for this module
logger = logging.getLogger('gnomonic_projection.base.transform')

class CoordinateTransformer:
    """
    Utility class for transforming coordinates between different systems.
    """

    @staticmethod
    def latlon_to_image_coords(
        lat: np.ndarray, 
        lon: np.ndarray, 
        config: Any, 
        shape: Tuple[int, int, ...]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert latitude and longitude to image coordinates.

        Args:
            lat (np.ndarray): Latitude values.
            lon (np.ndarray): Longitude values.
            config (Any): Configuration object containing grid parameters.
            shape (Tuple[int, int, ...]): Shape of the target image (height, width, ...).

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y coordinates in image space.

        Raises:
            TransformationError: If input arrays are invalid or computation fails.
            ConfigurationError: If config lacks required attributes.
        """
        logger.debug("Transforming latitude and longitude to image coordinates.")
        if not isinstance(lat, np.ndarray) or not isinstance(lon, np.ndarray):
            error_msg = "lat and lon must be NumPy ndarrays."
            logger.error(error_msg)
            raise TransformationError(error_msg)
        if not hasattr(config, "lon_min") or not hasattr(config, "lon_max") \
           or not hasattr(config, "lat_min") or not hasattr(config, "lat_max"):
            error_msg = "config must have 'lon_min', 'lon_max', 'lat_min', and 'lat_max' attributes."
            logger.error(error_msg)
            raise ConfigurationError(error_msg)

        if len(shape) < 2:
            error_msg = "Image shape must have at least two dimensions (height, width)."
            logger.error(error_msg)
            raise TransformationError(error_msg)

        H, W = shape[:2]
        try:
            map_x = (lon - config.lon_min) / (config.lon_max - config.lon_min) * (W - 1)
            map_y = (config.lat_max - lat) / (config.lat_max - config.lat_min) * (H - 1)
            logger.debug("Computed image coordinates successfully.")
        except Exception as e:
            error_msg = f"Failed to compute image coordinates: {e}"
            logger.exception(error_msg)
            raise TransformationError(error_msg) from e

        return map_x, map_y

    @staticmethod
    def xy_to_image_coords(
        x: np.ndarray, 
        y: np.ndarray, 
        config: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert X and Y grid coordinates to image coordinates.

        Args:
            x (np.ndarray): X coordinates in grid space.
            y (np.ndarray): Y coordinates in grid space.
            config (Any): Configuration object containing grid parameters.

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y coordinates in image space.

        Raises:
            TransformationError: If input arrays are invalid or computation fails.
        """
        logger.debug("Transforming grid coordinates (x, y) to image coordinates.")
        if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray):
            error_msg = "x and y must be NumPy ndarrays."
            logger.error(error_msg)
            raise TransformationError(error_msg)

        try:
            # Compute grid bounds dynamically based on FOV
            half_fov_rad = np.deg2rad(config.fov_deg / 2)
            x_max = np.tan(half_fov_rad) * config.R
            y_max = np.tan(half_fov_rad) * config.R
            x_min, y_min = -x_max, -y_max

            # Transform grid coordinates to image coordinates
            map_x = (x - x_min) / (x_max - x_min) * (config.x_points - 1)
            map_y = (y_max - y) / (y_max - y_min) * (config.y_points - 1)
            logger.debug("Grid coordinates transformed to image coordinates successfully.")
        except Exception as e:
            error_msg = f"Failed to compute image coordinates: {e}"
            logger.exception(error_msg)
            raise TransformationError(error_msg) from e

        return map_x, map_y