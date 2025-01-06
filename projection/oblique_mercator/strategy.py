# projection/oblique_mercator/strategy.py

import logging
import numpy as np
from typing import Tuple
from ..base.strategy import BaseProjectionStrategy
from ..exceptions import ProcessingError
from .config import ObliqueMercatorConfig

logger = logging.getLogger("projection.oblique_mercator.strategy")


class ObliqueMercatorProjectionStrategy(BaseProjectionStrategy):
    def __init__(self, config: ObliqueMercatorConfig) -> None:
        logger.debug("Initializing ObliqueMercatorProjectionStrategy.")
        self.config = config
        self.R = config.R
        self.phi_c = np.radians(config.center_lat)
        self.lam_c = np.radians(config.center_lon)
        self.azimuth = np.radians(config.azimuth_deg)

        self.phi_p = np.arcsin(np.cos(self.phi_c) * np.sin(self.azimuth))
        self.lam_p = np.arctan2(
            -np.cos(self.azimuth),
            -np.sin(self.phi_c) * np.sin(self.azimuth),
        ) + self.lam_c

    def from_spherical_to_projection(self, lat: np.ndarray, lon: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        logger.debug("Performing forward Oblique Mercator transformation.")
        try:
            lat_rad = np.radians(lat)
            lon_rad = np.radians(lon)

            A = np.sin(self.phi_p) * np.sin(lat_rad) - np.cos(self.phi_p) * np.cos(lat_rad) * np.sin(lon_rad - self.lam_p)
            x = self.R * np.arctan2(np.tan(self.phi_p) * np.cos(lat_rad) + np.sin(lat_rad) * np.sin(lon_rad - self.lam_p), np.cos(lon_rad - self.lam_p))
            y = self.R * 0.5 * np.log((1 + A) / (1 - A))
            mask = np.ones_like(x, dtype=bool)
            return x, y, mask
        except Exception as e:
            logger.exception(f"Forward transform error: {e}")
            raise ProcessingError(str(e))

    def from_projection_to_spherical(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        logger.debug("Performing inverse Oblique Mercator transformation.")
        try:
            A = np.sinh(y / self.R)
            lat_rad = np.arcsin(np.sin(self.phi_p) * A + np.cos(self.phi_p) * np.cosh(x / self.R))
            lon_rad = self.lam_p + np.arctan2(
                np.sinh(x / self.R),
                np.cos(self.phi_p) * A - np.sin(self.phi_p) * np.cosh(x / self.R),
            )
            return np.degrees(lat_rad), np.degrees(lon_rad)
        except Exception as e:
            logger.exception(f"Inverse transform error: {e}")
            raise ProcessingError(str(e))