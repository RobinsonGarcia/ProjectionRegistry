from .base.config import BaseProjectionConfig
from .base.transform import CoordinateTransformer
import cv2
import numpy as np
class ProjectionProcessor:
    def __init__(self, config: BaseProjectionConfig):
        self.config = config
        self.projection = config.create_projection()
        self.grid_generation = config.create_grid_generation()
        self.interpolation = config.create_interpolation()

    def forward(self, img: np.ndarray, **kwargs) -> np.ndarray:
        """
        Forward projection of an image.

        Args:
            img (np.ndarray): The input equirectangular image.
            **kwargs: Additional parameters to override projection configuration.

        Returns:
            np.ndarray: Projected rectilinear image.
        """
        # Update configuration with dynamic parameters
        self.config.update(**kwargs)

        # Generate grid
        x_grid, y_grid = self.grid_generation.create_grid('forward')

        # Forward projection
        lat, lon = self.projection.forward(x_grid, y_grid)

        # Transform lat/lon to image coordinates
        map_x, map_y = CoordinateTransformer.latlon_to_image_coords(lat, lon, self.grid_generation.config, img.shape)

        # Interpolate to get the rectilinear image
        return self.interpolation.interpolate(img, map_x, map_y)

    def backward(self, rect_img: np.ndarray, **kwargs) -> np.ndarray:
        """
        Backward projection of a rectilinear image to equirectangular.

        Args:
            rect_img (np.ndarray): The rectilinear image.
            img_shape (tuple): Shape of the equirectangular image (height, width).
            **kwargs: Additional parameters to override projection configuration.

        Returns:
            np.ndarray: Back-projected equirectangular image.
        """
        # Update configuration with dynamic parameters
        self.config.update(**kwargs)

        # Generate grid
        lon_grid, lat_grid = self.grid_generation.create_grid('backward')

        # Backward projection
        x, y, mask = self.projection.backward(lat_grid, lon_grid)

        # Transform (x, y) to image coordinates
        map_x, map_y = CoordinateTransformer.xy_to_image_coords(x, y, self.grid_generation.config)

        # Interpolate to get the equirectangular image
        back_projected_img = self.interpolation.interpolate(rect_img, map_x, map_y, mask if kwargs.get("return_mask", False) else None)

        return cv2.flip(back_projected_img * mask[:,:,None],0) 