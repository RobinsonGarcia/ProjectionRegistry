# /Users/robinsongarcia/projects/AzimutalEquidistant/projection/AzimutalEquidistant/strategy.py

from typing import Any, Tuple
from ..base.strategy import BaseProjectionStrategy
from .config import AzimutalEquidistantConfig
from ..exceptions import ProcessingError
import numpy as np
import logging

logger = logging.getLogger('AzimutalEquidistant_projection.AzimutalEquidistant.strategy')

class AzimutalEquidistantProjectionStrategy(BaseProjectionStrategy):
    """
    Projection Strategy for AzimutalEquidistant Projection.

    This class implements the transformation logic for both forward (Equirectangular to AzimutalEquidistant)
    and inverse (AzimutalEquidistant to Equirectangular) projections based on spherical trigonometry.
    It ensures accurate mapping between geographic coordinates and planar projection coordinates.
    """

    def __init__(self, config: AzimutalEquidistantConfig) -> None:
        """
        Initialize the AzimutalEquidistantProjectionStrategy with the given configuration.

        Args:
            config (AzimutalEquidistantConfig): The configuration object containing projection parameters.

        Raises:
            TypeError: If the config is not an instance of AzimutalEquidistantConfig.
        """
        logger.debug("Initializing AzimutalEquidistantProjectionStrategy.")
        if not isinstance(config, AzimutalEquidistantConfig):
            error_msg = f"config must be an instance of AzimutalEquidistantConfig, got {type(config)} instead."
            logger.error(error_msg)
            raise TypeError(error_msg)
        self.config: AzimutalEquidistantConfig = config
        logger.info("AzimutalEquidistantProjectionStrategy initialized successfully.")

    def from_projection_to_spherical(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:

        logger.debug("Starting inverse AzimutalEquidistant projection (Planar to Geographic).")
        try:
            phi1_rad, lam0_rad = np.deg2rad([self.config.phi1_deg, self.config.lam0_deg])
            logger.debug(f"Projection center (phi1_rad, lam0_rad): ({phi1_rad}, {lam0_rad})")

            rho = np.sqrt(x**2 + y**2)
            logger.debug("Computed rho (radial distances) from grid points.")

            c = rho / self.config.R
            sin_c, cos_c = np.sin(c), np.cos(c)
            logger.debug(f"Computed auxiliary angles c, sin_c, cos_c for rho.")

            phi = np.arcsin(cos_c * np.sin(phi1_rad) + (y * sin_c * np.cos(phi1_rad)) / rho)
            logger.debug("Computed latitude (phi) for inverse projection.")

            lam = lam0_rad + np.arctan2(
                x * sin_c,
                rho * np.cos(phi1_rad) * cos_c - y * np.sin(phi1_rad) * sin_c
            )
            logger.debug("Computed longitude (lambda) for inverse projection.")

            lat = np.rad2deg(phi)
            lon = np.rad2deg(lam)
            logger.debug("Converted phi and lambda from radians to degrees.")

            logger.debug("Inverse AzimutalEquidistant projection computed successfully.")
            return lat, lon
        except Exception as e:
            error_msg = f"Failed during inverse AzimutalEquidistant projection: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg) from e

    def from_spherical_to_projection(self, lat: np.ndarray, lon: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Perform forward AzimutalEquidistant projection from geographic coordinates to planar grid coordinates.

        Args:
            lat (np.ndarray): Latitude values in degrees.
            lon (np.ndarray): Longitude values in degrees.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: Arrays of X and Y planar coordinates and a mask indicating valid points.

        Raises:
            ProcessingError: If the projection computation fails.
        """
        logger.debug("Starting forward AzimutalEquidistant projection (Geographic to Planar).")
        try:
            phi1_rad, lam0_rad = np.deg2rad([self.config.phi1_deg, self.config.lam0_deg])
            logger.debug(f"Projection center (phi1_rad, lam0_rad): ({phi1_rad}, {lam0_rad})")

            phi_rad, lam_rad = np.deg2rad([lat, lon])
            logger.debug("Converted input lat/lon to radians.")

            cos_c = (
                np.sin(phi1_rad) * np.sin(phi_rad) +
                np.cos(phi1_rad) * np.cos(phi_rad) * np.cos(lam_rad - lam0_rad)
            )
            logger.debug("Computed cos_c for forward projection.")

            cos_c = np.where(cos_c == 0, 1e-10, cos_c)
            logger.debug("Adjusted cos_c to avoid division by zero.")

            sin_c = np.sqrt(1 - cos_c**2)
            k = np.arccos(cos_c) / sin_c

            x = self.config.R * np.cos(phi_rad) * np.sin(lam_rad - lam0_rad) * k
            logger.debug("Computed X planar coordinates for forward projection.")

            y = self.config.R * (
                np.cos(phi1_rad) * np.sin(phi_rad) -
                np.sin(phi1_rad) * np.cos(phi_rad) * np.cos(lam_rad - lam0_rad)
            ) * k
            logger.debug("Computed Y planar coordinates for forward projection.")

            mask = np.ones_like(cos_c) ==1 #cos_c > 0
            logger.debug("Generated mask for valid projection points (cos_c > 0).")

            logger.debug("Forward AzimutalEquidistant projection computed successfully.")
            return x, y, mask
        except Exception as e:
            error_msg = f"Failed during forward AzimutalEquidistant projection: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg) from e