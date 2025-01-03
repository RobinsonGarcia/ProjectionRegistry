from ..base.strategy import BaseProjectionStrategy
import numpy as np
import logging

logger = logging.getLogger('projection.mercator.strategy')

class MercatorProjectionStrategy(BaseProjectionStrategy):
    """
    Projection strategy for Mercator projection.
    """

    def __init__(self, config):
        if not hasattr(config, 'R'):
            raise ValueError("Config object must have the necessary attributes (e.g., 'R').")
        self.config = config  # Use the validated config object directly

    def forward(self, lon: np.ndarray, lat: np.ndarray):
        """
        Convert geographic coordinates to Cartesian coordinates for Mercator projection.

        Args:
            lon (np.ndarray): Longitudes (degrees).
            lat (np.ndarray): Latitudes (degrees).

        Returns:
            Tuple[np.ndarray, np.ndarray]: Projected x, y coordinates.
        """
        logger.debug("Starting Mercator forward projection.")
        try:
            
            # Calculate longitude and latitude
            lon = lon / self.config.R
            lat =  np.pi / 2 - 2 * np.arctan(np.e**(lat/ self.config.R))

            logger.debug("Mercator forward projection computed successfully.")
            print("MAX",lon.max(),lat.max())
            return lat, lon # (lat,lon)

        except Exception as e:
            logger.exception("Failed during Mercator forward projection.")
            raise ValueError(f"Mercator forward projection failed: {e}")

    def backward(self, x: np.ndarray, y: np.ndarray):
        """
        Convert Cartesian coordinates to geographic coordinates for Mercator projection.

        Args:
            x (np.ndarray): X coordinates.
            y (np.ndarray): Y coordinates.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: Longitudes, latitudes, and mask for valid coordinates.
        """
        logger.debug("Starting Mercator backward projection.")
        try:
            # Convert degrees to radians
            lon_rad = np.radians(x)
            lat_rad = np.radians(y)#_clamped)
            

            # Calculate x and y using Mercator projection formula
            # Calculate x and y using Mercator projection formula
            x = 1 * lon_rad
            y = 1 * np.log(np.tan(np.pi / 4 + lat_rad / 2))


            # Generate mask for valid coordinates
            mask = np.ones_like(x) == 1

            logger.debug("Mercator backward projection computed successfully.")
            return x, y, mask

        except Exception as e:
            logger.exception("Failed during Mercator backward projection.")
            raise ValueError(f"Mercator backward projection failed: {e}")