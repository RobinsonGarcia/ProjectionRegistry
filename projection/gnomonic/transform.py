from typing import Tuple, Any
import numpy as np
import logging
from ..exceptions import TransformationError, ConfigurationError

logger = logging.getLogger('projection.gnomonic.transform')

class GnomonicTransformer:
    """
    Transformation logic for Gnomonic projection.
    """
    def __init__(self, config):
        """
        Initialize the GnomonicTransformer with the given configuration.

        Args:
            config: Configuration object with necessary parameters.
        """
        if not hasattr(config, "lon_min") or not hasattr(config, "lon_max") \
           or not hasattr(config, "lat_min") or not hasattr(config, "lat_max") \
           or not hasattr(config, "fov_deg") or not hasattr(config, "R"):
            error_msg = "Configuration object is missing required attributes."
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
        
        self.config = config  # Store the configuration object
        logger.info("GnomonicTransformer initialized successfully.")

    def _validate_inputs(self, array: np.ndarray, name: str) -> None:
        """
        Validate input arrays to ensure they are NumPy arrays.

        Args:
            array (np.ndarray): Input array to validate.
            name (str): Name of the array for error messages.

        Raises:
            TransformationError: If the input is invalid.
        """
        if not isinstance(array, np.ndarray):
            error_msg = f"{name} must be a NumPy ndarray."
            logger.error(error_msg)
            raise TransformationError(error_msg)

    def _compute_image_coords(self, values: np.ndarray, min_val: float, max_val: float, size: int) -> np.ndarray:
        """
        Generalized method to compute normalized image coordinates.

        Args:
            values (np.ndarray): Input values (e.g., lat, lon, x, or y).
            min_val (float): Minimum value for normalization.
            max_val (float): Maximum value for normalization.
            size (int): Size of the target axis (width or height).

        Returns:
            np.ndarray: Normalized image coordinates.
        """
        return (values - min_val) / (max_val - min_val) * (size - 1)

    def latlon_to_image_coords(
        self, lat: np.ndarray, lon: np.ndarray, shape: Tuple[int, int]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert latitude and longitude to Gnomonic image coordinates.

        Args:
            lat (np.ndarray): Latitude values.
            lon (np.ndarray): Longitude values.
            shape (Tuple[int, int]): Shape of the target image (height, width).

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y coordinates in image space.

        Raises:
            TransformationError: If input arrays are invalid or computation fails.
        """
        logger.debug("Transforming latitude and longitude to image coordinates.")
        try:
            self._validate_inputs(lat, "lat")
            self._validate_inputs(lon, "lon")
            H, W = shape
            map_x = self._compute_image_coords(
                lon, self.config.lon_min, self.config.lon_max, W
            )
            map_y = self._compute_image_coords(
                lat, self.config.lat_max, self.config.lat_min, H
            )
            logger.debug("Latitude and longitude transformed successfully.")
            return map_x, map_y
        except Exception as e:
            logger.exception("Failed to transform latitude and longitude to image coordinates.")
            raise TransformationError(f"Gnomonic lat/lon transformation failed: {e}")

    def xy_to_image_coords(
        self, x: np.ndarray, y: np.ndarray, config: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Transform XY grid coordinates to image coordinates.

        Args:
            x (np.ndarray): X grid coordinates.
            y (np.ndarray): Y grid coordinates.
            config (Any): Configuration object.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Image coordinates.

        Raises:
            TransformationError: If input arrays are invalid or computation fails.
        """
        logger.debug("Transforming XY grid coordinates to image coordinates.")
        try:
            self._validate_inputs(x, "x")
            self._validate_inputs(y, "y")

            half_fov_rad = np.deg2rad(config.fov_deg / 2)
            x_max = np.tan(half_fov_rad) * config.R
            y_max = np.tan(half_fov_rad) * config.R
            x_min, y_min = -x_max, -y_max

            map_x = self._compute_image_coords(x, x_min, x_max, config.x_points)
            map_y = self._compute_image_coords(y, y_max, y_min, config.y_points)
            logger.debug("XY grid coordinates transformed successfully.")
            return map_x, map_y
        except Exception as e:
            logger.exception("Failed to transform XY grid coordinates to image coordinates.")
            raise TransformationError(f"Gnomonic XY transformation failed: {e}")