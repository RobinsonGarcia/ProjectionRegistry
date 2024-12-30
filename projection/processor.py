### /Users/robinsongarcia/projects/gnomonic/projection/processor.py ###

from typing import Any, Optional, Tuple
from .base.config import BaseProjectionConfig
from .base.transform import CoordinateTransformer
import cv2
import numpy as np

class ProjectionProcessor:
    """
    Processor for handling forward and backward projections using the provided configuration.
    """
    def __init__(self, config: BaseProjectionConfig) -> None:
        """
        Initialize the ProjectionProcessor with a given configuration.

        Args:
            config (BaseProjectionConfig): The projection configuration.

        Raises:
            TypeError: If 'config' is not an instance of BaseProjectionConfig.
            RuntimeError: If initialization of components fails.
        """
        if not isinstance(config, BaseProjectionConfig):
            raise TypeError(f"config must be an instance of BaseProjectionConfig, got {type(config)} instead.")
        
        self.config: BaseProjectionConfig = config
        try:
            self.projection = config.create_projection()
            self.grid_generation = config.create_grid_generation()
            self.interpolation = config.create_interpolation()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize ProjectionProcessor components: {e}") from e

    def forward(self, img: np.ndarray, **kwargs: Any) -> np.ndarray:
        """
        Forward projection of an image.

        Args:
            img (np.ndarray): The input equirectangular image.
            **kwargs (Any): Additional parameters to override projection configuration.

        Returns:
            np.ndarray: Projected rectilinear image.

        Raises:
            ValueError: If image is not a valid NumPy array.
            RuntimeError: If projection or grid generation fails.
        """
        if not isinstance(img, np.ndarray):
            raise ValueError("Input image must be a NumPy ndarray.")

        # Update configuration with dynamic parameters
        self.config.update(**kwargs)

        try:
            # Generate grid
            x_grid, y_grid = self.grid_generation.create_grid('forward')
        except Exception as e:
            raise RuntimeError(f"Failed to create forward grid: {e}") from e

        try:
            # Forward projection
            lat, lon = self.projection.forward(x_grid, y_grid)
        except Exception as e:
            raise RuntimeError(f"Failed during forward projection: {e}") from e

        try:
            # Transform lat/lon to image coordinates
            map_x, map_y = CoordinateTransformer.latlon_to_image_coords(
                lat, lon, self.grid_generation.config, img.shape
            )
        except Exception as e:
            raise RuntimeError(f"Failed to transform coordinates to image space: {e}") from e

        try:
            # Interpolate to get the rectilinear image
            return self.interpolation.interpolate(img, map_x, map_y)
        except Exception as e:
            raise RuntimeError(f"Interpolation failed: {e}") from e

    def backward(self, rect_img: np.ndarray, **kwargs: Any) -> np.ndarray:
        """
        Backward projection of a rectilinear image to equirectangular.

        Args:
            rect_img (np.ndarray): The rectilinear image.
            **kwargs (Any): Additional parameters to override projection configuration.

        Returns:
            np.ndarray: Back-projected equirectangular image.

        Raises:
            ValueError: If rect_img is not a valid NumPy array.
            RuntimeError: If projection, grid generation, or interpolation fails.
        """
        if not isinstance(rect_img, np.ndarray):
            raise ValueError("Rectilinear image must be a NumPy ndarray.")

        # Update configuration with dynamic parameters
        self.config.update(**kwargs)

        try:
            # Generate grid
            lon_grid, lat_grid = self.grid_generation.create_grid('backward')
        except Exception as e:
            raise RuntimeError(f"Failed to create backward grid: {e}") from e

        try:
            # Backward projection
            x, y, mask = self.projection.backward(lat_grid, lon_grid)
        except Exception as e:
            raise RuntimeError(f"Failed during backward projection: {e}") from e

        try:
            # Transform (x, y) to image coordinates
            map_x, map_y = CoordinateTransformer.xy_to_image_coords(x, y, self.grid_generation.config)
        except Exception as e:
            raise RuntimeError(f"Failed to transform (x, y) to image coordinates: {e}") from e

        try:
            # Interpolate to get the equirectangular image
            back_projected_img = self.interpolation.interpolate(
                rect_img, map_x, map_y, mask if kwargs.get("return_mask", False) else None
            )
        except Exception as e:
            raise RuntimeError(f"Interpolation failed: {e}") from e

        try:
            # Apply mask and flip image vertically if mask is provided
            if mask is None:
                raise ValueError("Mask is requested but not provided.")
            if not isinstance(mask, np.ndarray):
                raise ValueError("Mask must be a NumPy ndarray.")
            if mask.shape != back_projected_img.shape[:2]:
                raise ValueError("Mask shape must match the first two dimensions of the back_projected_img.")
            back_projected_img *= mask[:, :, None]
            return cv2.flip(back_projected_img, 0)
        except Exception as e:
            raise RuntimeError(f"Failed to finalize back-projected image: {e}") from e