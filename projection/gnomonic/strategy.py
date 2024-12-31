from typing import Any, Tuple
from ..base.strategy import BaseProjectionStrategy
from .config import GnomonicConfig
from ..exceptions import ProcessingError
import numpy as np
import logging

logger = logging.getLogger('gnomonic_projection.gnomonic.strategy')

class GnomonicProjectionStrategy(BaseProjectionStrategy):
    def __init__(self, config: GnomonicConfig) -> None:
        logger.debug("Initializing GnomonicProjectionStrategy.")
        if not isinstance(config, GnomonicConfig):
            error_msg = f"config must be an instance of GnomonicConfig, got {type(config)} instead."
            logger.error(error_msg)
            raise TypeError(error_msg)
        self.config: GnomonicConfig = config
        logger.info("GnomonicProjectionStrategy initialized successfully.")

    def forward(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        logger.debug("Starting forward Gnomonic projection.")
        try:
            phi1_rad, lam0_rad = np.deg2rad([self.config.phi1_deg, self.config.lam0_deg])
            rho = np.sqrt(x**2 + y**2)
            c = np.arctan2(rho, self.config.R)
            sin_c, cos_c = np.sin(c), np.cos(c)
            phi = np.arcsin(cos_c * np.sin(phi1_rad) - (y * sin_c * np.cos(phi1_rad)) / rho)
            lam = lam0_rad + np.arctan2(x * sin_c, rho * np.cos(phi1_rad) * cos_c + y * np.sin(phi1_rad) * sin_c)
            lat = np.rad2deg(phi)
            lon = np.rad2deg(lam)
            logger.debug("Forward Gnomonic projection computed successfully.")
            return lat, lon
        except Exception as e:
            error_msg = f"Failed during forward Gnomonic projection: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg) from e

    def backward(self, lat: np.ndarray, lon: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        logger.debug("Starting backward Gnomonic projection.")
        try:
            phi1_rad, lam0_rad = np.deg2rad([self.config.phi1_deg, self.config.lam0_deg])
            phi_rad, lam_rad = np.deg2rad([lat, lon])
            cos_c = np.sin(phi1_rad) * np.sin(phi_rad) + np.cos(phi1_rad) * np.cos(phi_rad) * np.cos(lam_rad - lam0_rad)
            cos_c = np.where(cos_c == 0, 1e-10, cos_c)
            x = self.config.R * np.cos(phi_rad) * np.sin(lam_rad - lam0_rad) / cos_c
            y = self.config.R * (np.cos(phi1_rad) * np.sin(phi_rad) - np.sin(phi1_rad) * np.cos(phi_rad) * np.cos(lam_rad - lam0_rad)) / cos_c
            mask = cos_c > 0
            logger.debug("Backward Gnomonic projection computed successfully.")
            return x, y, mask
        except Exception as e:
            error_msg = f"Failed during backward Gnomonic projection: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg) from e