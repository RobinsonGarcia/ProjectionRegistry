### /Users/robinsongarcia/projects/gnomonic/projection/gnomonic/strategy.py ###

from typing import Any, Tuple
from ..base.strategy import BaseProjectionStrategy
from .config import GnomonicConfig
import numpy as np

class GnomonicProjectionStrategy(BaseProjectionStrategy):
    """
    Gnomonic projection strategy implementing forward and backward transformations.
    """
    def __init__(self, config: GnomonicConfig) -> None:
        """
        Initialize the GnomonicProjectionStrategy with the provided configuration.

        Args:
            config (GnomonicConfig): The Gnomonic projection configuration.

        Raises:
            TypeError: If 'config' is not an instance of GnomonicConfig.
        """
        if not isinstance(config, GnomonicConfig):
            raise TypeError(f"config must be an instance of GnomonicConfig, got {type(config)} instead.")
        self.config: GnomonicConfig = config

    def forward(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform forward Gnomonic projection from grid coordinates to latitude and longitude.

        Args:
            x (np.ndarray): X-coordinates in the grid.
            y (np.ndarray): Y-coordinates in the grid.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Arrays of latitude and longitude in degrees.

        Raises:
            ValueError: If input arrays are not valid NumPy ndarrays.
            RuntimeError: If projection computation fails.
        """
        if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray):
            raise ValueError("x and y must be NumPy ndarrays.")

        try:
            phi1_rad, lam0_rad = np.deg2rad([self.config.phi1_deg, self.config.lam0_deg])
            rho = np.sqrt(x**2 + y**2)
            c = np.arctan2(rho, self.config.R)
            sin_c, cos_c = np.sin(c), np.cos(c)
            phi = np.arcsin(cos_c * np.sin(phi1_rad) - (y * sin_c * np.cos(phi1_rad)) / rho)
            lam = lam0_rad + np.arctan2(x * sin_c, rho * np.cos(phi1_rad) * cos_c + y * np.sin(phi1_rad) * sin_c)
            return np.rad2deg(phi), np.rad2deg(lam)
        except Exception as e:
            raise RuntimeError(f"Failed during forward Gnomonic projection: {e}") from e

    def backward(self, lat: np.ndarray, lon: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Perform backward Gnomonic projection from latitude and longitude to grid coordinates.

        Args:
            lat (np.ndarray): Latitude values in degrees.
            lon (np.ndarray): Longitude values in degrees.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: X and Y coordinates in grid space, and a mask array indicating valid projections.

        Raises:
            ValueError: If input arrays are not valid NumPy ndarrays.
            RuntimeError: If projection computation fails.
        """
        if not isinstance(lat, np.ndarray) or not isinstance(lon, np.ndarray):
            raise ValueError("lat and lon must be NumPy ndarrays.")

        try:
            phi1_rad, lam0_rad = np.deg2rad([self.config.phi1_deg, self.config.lam0_deg])
            phi_rad, lam_rad = np.deg2rad([lat, lon])
            cos_c = np.sin(phi1_rad) * np.sin(phi_rad) + np.cos(phi1_rad) * np.cos(phi_rad) * np.cos(lam_rad - lam0_rad)
            # Avoid division by zero
            cos_c = np.where(cos_c == 0, 1e-10, cos_c)
            x = self.config.R * np.cos(phi_rad) * np.sin(lam_rad - lam0_rad) / cos_c
            y = self.config.R * (np.cos(phi1_rad) * np.sin(phi_rad) - np.sin(phi1_rad) * np.cos(phi_rad) * np.cos(lam_rad - lam0_rad)) / cos_c
            mask = cos_c > 0
            return x, y, mask
        except Exception as e:
            raise RuntimeError(f"Failed during backward Gnomonic projection: {e}") from e