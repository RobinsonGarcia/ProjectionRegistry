### /Users/robinsongarcia/projects/gnomonic/projection/gnomonic/grid.py ###

from typing import Any, Tuple
from ..base.grid import BaseGridGeneration
from .config import GnomonicConfig
import numpy as np

class GnomonicGridGeneration(BaseGridGeneration):
    """
    Grid generation implementation for Gnomonic projections.
    """
    def __init__(self, config: GnomonicConfig) -> None:
        """
        Initialize the grid generation with the provided configuration.

        Args:
            config (GnomonicConfig): The Gnomonic projection configuration.

        Raises:
            TypeError: If 'config' is not an instance of GnomonicConfig.
        """
        if not isinstance(config, GnomonicConfig):
            raise TypeError(f"config must be an instance of GnomonicConfig, got {type(config)} instead.")
        self.config: GnomonicConfig = config

    def create_grid(self, direction: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create a grid based on the specified direction.

        Args:
            direction (str): Direction of grid creation ('forward' or 'backward').

        Returns:
            Tuple[np.ndarray, np.ndarray]: Generated grid arrays.

        Raises:
            ValueError: If the direction is invalid.
            RuntimeError: If grid creation fails.
        """
        if direction == 'forward':
            try:
                x_vals = np.linspace(self.config.x_min, self.config.x_max, self.config.x_points)
                y_vals = np.linspace(self.config.y_min, self.config.y_max, self.config.y_points)
                return np.meshgrid(x_vals, y_vals)
            except Exception as e:
                raise RuntimeError(f"Failed to create forward grid: {e}") from e
        elif direction == 'backward':
            try:
                lon_vals = np.linspace(self.config.lon_min, self.config.lon_max, self.config.lon_points)
                lat_vals = np.linspace(self.config.lat_min, self.config.lat_max, self.config.lat_points)
                return np.meshgrid(lon_vals, lat_vals)
            except Exception as e:
                raise RuntimeError(f"Failed to create backward grid: {e}") from e
        else:
            raise ValueError("Direction must be 'forward' or 'backward'.")