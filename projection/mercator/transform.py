from typing import Tuple, Any
import numpy as np
import logging
from ..exceptions import TransformationError

logger = logging.getLogger('projection.mercator.transform')

class MercatorTransformer:
    """
    Transformation logic for Mercator projection.
    """
    def __init__(self, config):
        """
        Initialize the GnomonicTransformer with the given configuration.

        Args:
            config: Configuration object with necessary parameters.
        """
        self.config = config  # Store the configuration object for use in transformations
        
    @staticmethod
    def latlon_to_image_coords(
        lat: np.ndarray, 
        lon: np.ndarray, 
        config: Any, 
        shape: Tuple[int, int]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert latitude and longitude to Mercator image coordinates.

        Args:
            lat (np.ndarray): Latitude values.
            lon (np.ndarray): Longitude values.
            config (Any): Configuration object containing grid parameters.
            shape (Tuple[int, int]): Shape of the target image (height, width).

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y coordinates in image space.

        Raises:
            TransformationError: If input arrays are invalid or computation fails.
        """
        logger.debug("Transforming lat/lon to Mercator image coordinates.")
        try:
            H, W = shape
            map_x = (lon - config.lon_min) / (config.lon_max - config.lon_min) * (W - 1)

            lat_rad = np.radians(lat)
            lat_min_rad = np.radians(config.lat_min)
            lat_max_rad = np.radians(config.lat_max)
            map_y = (
                np.log(np.tan(np.pi / 4 + lat_rad / 2)) -
                np.log(np.tan(np.pi / 4 + lat_min_rad / 2))
            ) / (
                np.log(np.tan(np.pi / 4 + lat_max_rad / 2)) -
                np.log(np.tan(np.pi / 4 + lat_min_rad / 2))
            ) * (H - 1)

            return map_x, map_y
        except Exception as e:
            logger.exception("Failed to transform coordinates for Mercator projection.")
            raise TransformationError(f"Mercator transformation failed: {e}")

    @staticmethod
    def xy_to_image_coords(
        x: np.ndarray, 
        y: np.ndarray, 
        config: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Transform XY grid coordinates to Mercator image coordinates.

        Args:
            x (np.ndarray): X grid coordinates.
            y (np.ndarray): Y grid coordinates.
            config (Any): Configuration object.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Image coordinates.
        """
        raise NotImplementedError("Mercator backward transformation is not required.")