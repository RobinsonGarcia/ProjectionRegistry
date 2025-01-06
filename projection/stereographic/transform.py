# projection/stereographic/transform.py

import logging
import numpy as np
from typing import Tuple, Any
from ..base.transform import BaseCoordinateTransformer
from ..exceptions import TransformationError, ConfigurationError

logger = logging.getLogger("projection.stereographic.transform")


class StereographicTransformer(BaseCoordinateTransformer):
    """
    Convert lat/lon or x/y in Stereographic projection to final image pixel coords.
    """

    def __init__(self, config: Any):
        super().__init__(config)
        logger.debug("Initializing StereographicTransformer.")
        # Validate needed attributes
        required = ["lon_min", "lon_max", "lat_min", "lat_max", "x_points", "y_points", "R", "scaling_factor"]
        missing = [attr for attr in required if not hasattr(config, attr)]
        if missing:
            error_msg = f"Config missing attributes: {', '.join(missing)}"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
        logger.info("StereographicTransformer initialized successfully.")

    def spherical_to_image_coords(
        self, lat: np.ndarray, lon: np.ndarray, shape: Tuple[int, int]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert lat/lon (degrees) to image pixel indices.
        shape is typically (height, width) of the input image.
        """
        logger.debug("Starting Stereographic spherical_to_image_coords.")
        H, W = shape
        lon[lon>180] = 180 - lon[lon>180]
        lat[lat>90] = 90 - lat[lat>90]

        # Assuming linear scaling for simplicity; adjust as needed
        map_x = (lon - self.config.lon_min) / (self.config.lon_max - self.config.lon_min) * (W - 1)
        map_y = (self.config.lat_max - lat) / (self.config.lat_max - self.config.lat_min) * (H - 1)

        logger.debug("Mapped spherical coordinates to image pixel coordinates.")
        return map_x, map_y

    def projection_to_image_coords(
        self, x: np.ndarray, y: np.ndarray, config: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert Stereographic projection-plane (x, y) to pixel coordinates.
        """
        logger.debug("Starting Stereographic projection_to_image_coords.")
        # Define the maximum extent based on scaling factor and radius
        max_extent = 2 * config.R * config.scaling_factor  # Typically covers the hemisphere
        min_extent = -max_extent

        map_x = ((x - min_extent) / (2 * max_extent)) * (config.x_points - 1)
        map_y = ((max_extent - y) / (2 * max_extent)) * (config.y_points - 1)

        logger.debug("Mapped projection coordinates to image pixel coordinates.")
        return map_x, map_y