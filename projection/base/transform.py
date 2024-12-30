### /Users/robinsongarcia/projects/gnomonic/projection/base/transform.py ###

from typing import Any, Tuple
import numpy as np

class CoordinateTransformer:
    """
    Utility class for transforming coordinates between different systems.
    """
    @staticmethod
    def latlon_to_image_coords(
        lat: np.ndarray, 
        lon: np.ndarray, 
        config: Any, 
        shape: Tuple[int, int, ...]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert latitude and longitude to image coordinates.

        Args:
            lat (np.ndarray): Latitude values.
            lon (np.ndarray): Longitude values.
            config (Any): Configuration object containing grid parameters.
            shape (Tuple[int, int, ...]): Shape of the target image (height, width, ...).

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y coordinates in image space.

        Raises:
            ValueError: If input arrays are not compatible with the image shape.
            AttributeError: If config lacks required attributes.
        """
        if not isinstance(lat, np.ndarray) or not isinstance(lon, np.ndarray):
            raise ValueError("lat and lon must be NumPy ndarrays.")
        if not hasattr(config, "lon_min") or not hasattr(config, "lon_max") \
           or not hasattr(config, "lat_min") or not hasattr(config, "lat_max"):
            raise AttributeError("config must have 'lon_min', 'lon_max', 'lat_min', and 'lat_max' attributes.")

        if len(shape) < 2:
            raise ValueError("Image shape must have at least two dimensions (height, width).")

        H, W = shape[:2]
        try:
            map_x = (lon - config.lon_min) / (config.lon_max - config.lon_min) * (W - 1)
            map_y = (config.lat_max - lat) / (config.lat_max - config.lat_min) * (H - 1)
        except Exception as e:
            raise ValueError(f"Failed to compute image coordinates: {e}") from e

        return map_x, map_y

    @staticmethod
    def xy_to_image_coords(
        x: np.ndarray, 
        y: np.ndarray, 
        config: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert X and Y grid coordinates to image coordinates.

        Args:
            x (np.ndarray): X coordinates in grid space.
            y (np.ndarray): Y coordinates in grid space.
            config (Any): Configuration object containing grid parameters.

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y coordinates in image space.

        Raises:
            ValueError: If input arrays are not compatible with grid configuration.
            AttributeError: If config lacks required attributes.
        """
        if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray):
            raise ValueError("x and y must be NumPy ndarrays.")
        required_attrs = ["x_min", "x_max", "x_points", "y_min", "y_max", "y_points"]
        for attr in required_attrs:
            if not hasattr(config, attr):
                raise AttributeError(f"config must have '{attr}' attribute.")

        try:
            map_x = (x - config.x_min) / (config.x_max - config.x_min) * (config.x_points - 1)
            map_y = (config.y_max - y) / (config.y_max - config.y_min) * (config.y_points - 1)
        except Exception as e:
            raise ValueError(f"Failed to compute image coordinates: {e}") from e

        return map_x, map_y