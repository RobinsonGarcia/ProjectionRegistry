### /Users/robinsongarcia/projects/gnomonic/projection/base/interpolation.py ###

from typing import Any, Optional
import cv2
import numpy as np

class BaseInterpolation:
    """
    Base class for image interpolation in projections.
    """
    def __init__(self, config: Any) -> None:
        """
        Initialize the interpolation with the given configuration.

        Args:
            config (Any): The projection configuration.

        Raises:
            TypeError: If 'config' does not have required attributes.
        """
        if not hasattr(config, "interpolation") or not hasattr(config, "borderMode") or not hasattr(config, "borderValue"):
            raise TypeError("Config must have 'interpolation', 'borderMode', and 'borderValue' attributes.")
        self.config: Any = config

    def interpolate(
        self, 
        input_img: np.ndarray, 
        map_x: np.ndarray, 
        map_y: np.ndarray, 
        mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Perform image interpolation based on the provided mapping.

        Args:
            input_img (np.ndarray): The input image to interpolate.
            map_x (np.ndarray): The mapping for the x-coordinates.
            map_y (np.ndarray): The mapping for the y-coordinates.
            mask (Optional[np.ndarray], optional): Mask to apply to the interpolated image. Defaults to None.

        Returns:
            np.ndarray: The interpolated image.

        Raises:
            ValueError: If input images are not valid NumPy arrays.
            cv2.error: If OpenCV remap function fails.
        """
        if not isinstance(input_img, np.ndarray):
            raise ValueError("input_img must be a NumPy ndarray.")
        if not isinstance(map_x, np.ndarray) or not isinstance(map_y, np.ndarray):
            raise ValueError("map_x and map_y must be NumPy ndarrays.")

        try:
            map_x_32: np.ndarray = map_x.astype(np.float32)
            map_y_32: np.ndarray = map_y.astype(np.float32)
        except Exception as e:
            raise ValueError(f"Failed to convert map_x or map_y to float32: {e}") from e

        try:
            result: np.ndarray = cv2.remap(
                input_img, map_x_32, map_y_32,
                interpolation=self.config.interpolation,
                borderMode=self.config.borderMode,
                borderValue=self.config.borderValue
            )
        except cv2.error as e:
            raise cv2.error(f"OpenCV remap failed: {e}") from e

        if mask is not None:
            if not isinstance(mask, np.ndarray):
                raise ValueError("mask must be a NumPy ndarray if provided.")
            if mask.shape != result.shape[:2]:
                raise ValueError("mask shape must match the first two dimensions of the result.")
            result *= mask[:, :, None]

        return result