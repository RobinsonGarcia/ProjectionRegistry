### /Users/robinsongarcia/projects/gnomonic/projection/processor.py ###

from typing import Any, Optional, Tuple
from .base.config import BaseProjectionConfig
from .base.transform import CoordinateTransformer
from .exceptions import ProcessingError, InterpolationError, GridGenerationError, TransformationError
import logging
import cv2
import numpy as np

# Initialize logger for this module
logger = logging.getLogger('gnomonic_projection.processor')

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
            ProcessingError: If initialization of components fails.
        """
        logger.debug("Initializing ProjectionProcessor.")
        if not isinstance(config, BaseProjectionConfig):
            error_msg = f"config must be an instance of BaseProjectionConfig, got {type(config)} instead."
            logger.error(error_msg)
            raise TypeError(error_msg)
        
        self.config: BaseProjectionConfig = config
        try:
            self.projection = config.create_projection()
            self.grid_generation = config.create_grid_generation()
            self.interpolation = config.create_interpolation()
            logger.info("ProjectionProcessor components initialized successfully.")
        except Exception as e:
            error_msg = f"Failed to initialize ProjectionProcessor components: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg) from e

    def forward(self, img: np.ndarray, **kwargs: Any) -> np.ndarray:
        """
        Forward projection of an image.

        Args:
            img (np.ndarray): The input equirectangular image.
            **kwargs (Any): Additional parameters to override projection configuration.

        Returns:
            np.ndarray: Projected rectilinear image.

        Raises:
            InterpolationError: If interpolation fails.
            GridGenerationError: If grid generation fails.
            ProcessingError: If projection fails.
            ValueError: If image is not a valid NumPy array.
        """
        logger.debug("Starting forward projection.")
        if not isinstance(img, np.ndarray):
            error_msg = "Input image must be a NumPy ndarray."
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Update configuration with dynamic parameters
        self.config.update(**kwargs)
        logger.debug(f"Configuration updated with parameters: {kwargs}")

        try:
            # Generate grid
            x_grid, y_grid = self.grid_generation.create_grid('forward')
            logger.debug("Forward grid generated successfully.")
        except Exception as e:
            error_msg = f"Failed to create forward grid: {e}"
            logger.exception(error_msg)
            raise GridGenerationError(error_msg) from e

        try:
            # Forward projection
            lat, lon = self.projection.forward(x_grid, y_grid)
            logger.debug("Forward projection computed successfully.")
        except Exception as e:
            error_msg = f"Failed during forward projection: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg) from e

        try:
            # Transform lat/lon to image coordinates
            map_x, map_y = CoordinateTransformer.latlon_to_image_coords(
                lat, lon, self.grid_generation.config, img.shape
            )
            logger.debug("Coordinates transformed to image space successfully.")
        except Exception as e:
            error_msg = f"Failed to transform coordinates to image space: {e}"
            logger.exception(error_msg)
            raise TransformationError(error_msg) from e

        try:
            # Interpolate to get the rectilinear image
            projected_img = self.interpolation.interpolate(img, map_x, map_y)
            logger.debug("Image interpolation completed successfully.")
            return projected_img
        except Exception as e:
            error_msg = f"Interpolation failed: {e}"
            logger.exception(error_msg)
            raise InterpolationError(error_msg) from e

    def backward(self, rect_img: np.ndarray, **kwargs: Any) -> np.ndarray:
        """
        Backward projection of a rectilinear image to equirectangular.

        Args:
            rect_img (np.ndarray): The rectilinear image.
            **kwargs (Any): Additional parameters to override projection configuration.

        Returns:
            np.ndarray: Back-projected equirectangular image.

        Raises:
            InterpolationError: If interpolation fails.
            GridGenerationError: If grid generation fails.
            ProcessingError: If projection fails.
            TransformationError: If coordinate transformation fails.
            ValueError: If rect_img is not a valid NumPy array.
        """
        logger.debug("Starting backward projection.")
        if not isinstance(rect_img, np.ndarray):
            error_msg = "Rectilinear image must be a NumPy ndarray."
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Update configuration with dynamic parameters
        self.config.update(**kwargs)
        logger.debug(f"Configuration updated with parameters: {kwargs}")

        try:
            # Generate grid
            lon_grid, lat_grid = self.grid_generation.create_grid('backward')
            logger.debug("Backward grid generated successfully.")
        except Exception as e:
            error_msg = f"Failed to create backward grid: {e}"
            logger.exception(error_msg)
            raise GridGenerationError(error_msg) from e

        try:
            # Backward projection
            x, y, mask = self.projection.backward(lat_grid, lon_grid)
            logger.debug("Backward projection computed successfully.")
        except Exception as e:
            error_msg = f"Failed during backward projection: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg) from e

        try:
            # Transform (x, y) to image coordinates
            map_x, map_y = CoordinateTransformer.xy_to_image_coords(x, y, self.grid_generation.config)
            logger.debug("Grid coordinates transformed to image space successfully.")
        except Exception as e:
            error_msg = f"Failed to transform (x, y) to image coordinates: {e}"
            logger.exception(error_msg)
            raise TransformationError(error_msg) from e

        try:
            # Interpolate to get the equirectangular image
            back_projected_img = self.interpolation.interpolate(
                rect_img, map_x, map_y, mask if kwargs.get("return_mask", False) else None
            )
            logger.debug("Image interpolation for backward projection completed successfully.")
        except Exception as e:
            error_msg = f"Interpolation failed: {e}"
            logger.exception(error_msg)
            raise InterpolationError(error_msg) from e

        try:
            # Apply mask and flip image vertically if mask is provided
            if kwargs.get("return_mask", False):
                if mask is None:
                    error_msg = "Mask is requested but not provided."
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                if not isinstance(mask, np.ndarray):
                    error_msg = "Mask must be a NumPy ndarray."
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                if mask.shape != back_projected_img.shape[:2]:
                    error_msg = "Mask shape must match the first two dimensions of the back_projected_img."
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                back_projected_img *= mask[:, :, None]
                logger.debug("Mask applied to back-projected image successfully.")
            back_projected_img_flipped = cv2.flip(back_projected_img, 0)
            logger.debug("Back-projected image flipped vertically successfully.")
            return back_projected_img_flipped
        except Exception as e:
            error_msg = f"Failed to finalize back-projected image: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg) from e