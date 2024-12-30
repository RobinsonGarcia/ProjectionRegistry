### /Users/robinsongarcia/projects/gnomonic/projection/base/strategy.py ###

from typing import Any, Tuple
import numpy as np

class BaseProjectionStrategy:
    """
    Base class for projection strategies.
    """
    def forward(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform forward projection from grid coordinates to latitude and longitude.

        Args:
            x (np.ndarray): X-coordinates in the grid.
            y (np.ndarray): Y-coordinates in the grid.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Latitude and longitude arrays.

        Raises:
            NotImplementedError: If the method is not overridden by subclasses.
            ValueError: If inputs are not valid NumPy arrays.
        """
        if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray):
            raise ValueError("x and y must be NumPy ndarrays.")
        raise NotImplementedError("Subclasses must implement forward.")

    def backward(self, lat: np.ndarray, lon: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Perform backward projection from latitude and longitude to grid coordinates.

        Args:
            lat (np.ndarray): Latitude values.
            lon (np.ndarray): Longitude values.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: X and Y coordinates in the grid, and a mask array.

        Raises:
            NotImplementedError: If the method is not overridden by subclasses.
            ValueError: If inputs are not valid NumPy arrays.
        """
        if not isinstance(lat, np.ndarray) or not isinstance(lon, np.ndarray):
            raise ValueError("lat and lon must be NumPy ndarrays.")
        raise NotImplementedError("Subclasses must implement backward.")