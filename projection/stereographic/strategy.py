# projection/stereographic/strategy.py

import logging
import numpy as np
from typing import Tuple
from ..base.strategy import BaseProjectionStrategy
from .config import StereographicConfig
from ..exceptions import ProcessingError

logger = logging.getLogger("projection.stereographic.strategy")


class StereographicProjectionStrategy(BaseProjectionStrategy):
    """
    Implements forward (lat/lon -> x/y) and inverse (x/y -> lat/lon)
    transformations for Stereographic projection.
    """

    def __init__(self, config: StereographicConfig) -> None:
        """
        Initialize with validated config.
        """
        logger.debug("Initializing StereographicProjectionStrategy.")
        if not isinstance(config, StereographicConfig):
            error_msg = f"config must be StereographicConfig, got {type(config)}"
            logger.error(error_msg)
            raise TypeError(error_msg)
        self.config = config
        logger.info("StereographicProjectionStrategy initialized successfully.")

    def from_spherical_to_projection(
        self, lat: np.ndarray, lon: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Forward: lat/lon (degrees) -> x/y (units).
        Return (x, y, mask).
        """
        logger.debug("Starting forward Stereographic transformation.")
        try:
            phi0 = np.deg2rad(self.config.phi0_deg)
            lam0 = np.deg2rad(self.config.lam0_deg)

            phi = np.deg2rad(lat)
            lam = np.deg2rad(lon)

            # Compute the stereographic projection
            k = 2 * self.config.R / (1 + np.sin(phi0) * np.sin(phi) + 
                                     np.cos(phi0) * np.cos(phi) * np.cos(lam - lam0))
            x = k * np.cos(phi) * np.sin(lam - lam0) * self.config.scaling_factor
            y = k * (np.cos(phi0) * np.sin(phi) - np.sin(phi0) * np.cos(phi) * np.cos(lam - lam0)) * self.config.scaling_factor

            # Mask for points where projection is not defined
            mask = (1 + np.sin(phi0) * np.sin(phi) + 
                    np.cos(phi0) * np.cos(phi) * np.cos(lam - lam0)) > 0

            logger.debug("Forward Stereographic projection computed successfully.")
            return x, y, mask
        except Exception as e:
            error_msg = f"Forward Stereographic projection error: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg)

    def from_projection_to_spherical(
        self, x: np.ndarray, y: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Inverse: x/y -> lat/lon (degrees).
        """
        logger.debug("Starting inverse Stereographic transformation.")
        try:
            phi0 = np.deg2rad(self.config.phi0_deg)
            lam0 = np.deg2rad(self.config.lam0_deg)

            x_scaled = x / self.config.scaling_factor
            y_scaled = y / self.config.scaling_factor

            rho = np.sqrt(x_scaled**2 + y_scaled**2)
            c = 2 * np.arctan(rho / (2 * self.config.R))

            sin_c = np.sin(c)
            cos_c = np.cos(c)

            phi = np.arcsin(cos_c * np.sin(phi0) + (y_scaled * sin_c * np.cos(phi0)) / rho)
            lam = lam0 + np.arctan2(x_scaled * sin_c, rho * np.cos(phi0) * cos_c - y_scaled * np.sin(phi0) * sin_c)

            lat = np.rad2deg(phi)
            lon = np.rad2deg(lam)

            mask = cos_c > 0

            logger.debug("Inverse Stereographic projection computed successfully.")
            return lat, lon
        except Exception as e:
            error_msg = f"Inverse Stereographic projection error: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg)