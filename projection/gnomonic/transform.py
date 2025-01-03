from typing import Tuple, Any
import numpy as np
import logging
from ..exceptions import TransformationError, ConfigurationError

logger = logging.getLogger('projection.gnomonic.transform')

class GnomonicTransformer:
    """
    Transformation logic for Gnomonic projection.

    This class handles the conversion between geographic coordinates (latitude and longitude)
    and image coordinates on the projection plane. It utilizes the mathematical equations
    derived from spherical trigonometry to perform accurate mappings essential for both
    forward and backward projections.

    ## Mathematical Overview:

    The transformation leverages the following key equations derived from the Gnomonic projection:

    - **Latitude and Longitude to Image Coordinates:**

      $$
      x = \frac{a \,\sin \psi \,\cos \phi \,\sin(\lambda - \lambda_0)}{\sin \phi_0 \,\sin \phi + \cos \phi_0 \,\cos \phi \,\cos(\lambda - \lambda_0)}
      $$

      $$
      y = \frac{a \,\sin \psi \bigl[\cos \phi_0 \,\sin \phi - \sin \phi_0 \,\cos \phi \,\cos(\lambda - \lambda_0)\bigr]}{\sin \phi_0 \,\sin \phi + \cos \phi_0 \,\cos \phi \,\cos(\lambda - \lambda_0)}
      $$

    - **Image Coordinates to Latitude and Longitude:**

      Inverse transformations are applied to map image coordinates back to geographic coordinates,
      ensuring that the projection maintains accuracy and consistency.

    These equations ensure that great circles on the sphere map to straight lines on the projection plane,
    which is a defining characteristic of the Gnomonic projection.

    ## Special Considerations:

    - **Field of View (FOV):**
      
      The field of view (`fov_deg`) determines the extent of the sphere that is projected onto the plane.
      A larger FOV results in more distortion but covers a broader area.

    - **Projection Center:**
      
      The projection is centered at \((\phi_0, \lambda_0)\), allowing for oblique projections that are not
      limited to polar or equatorial orientations.

    ## Usage:

    This transformer should be used in conjunction with grid generation and projection strategy
    classes to accurately map between geographic and image coordinates during projection processes.
    """

    def __init__(self, config):
        """
        Initialize the GnomonicTransformer with the given configuration.

        Args:
            config: Configuration object containing necessary projection parameters.

        Raises:
            ConfigurationError: If the configuration object lacks required attributes.
        """
        required_attributes = ["lon_min", "lon_max", "lat_min", "lat_max", "fov_deg", "R", "x_points", "y_points"]
        missing_attributes = [attr for attr in required_attributes if not hasattr(config, attr)]

        if missing_attributes:
            error_msg = f"Configuration object is missing required attributes: {', '.join(missing_attributes)}"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)

        self.config = config  # Store the configuration object
        logger.info("GnomonicTransformer initialized successfully.")

    def _validate_inputs(self, array: np.ndarray, name: str) -> None:
        """
        Validate input arrays to ensure they are NumPy arrays.

        Args:
            array (np.ndarray): Input array to validate.
            name (str): Name of the array for error messages.

        Raises:
            TransformationError: If the input is invalid.
        """
        if not isinstance(array, np.ndarray):
            error_msg = f"{name} must be a NumPy ndarray."
            logger.error(error_msg)
            raise TransformationError(error_msg)

    def _compute_image_coords(self, values: np.ndarray, min_val: float, max_val: float, size: int) -> np.ndarray:
        """
        Generalized method to compute normalized image coordinates.

        Args:
            values (np.ndarray): Input values (e.g., lat, lon, x, or y).
            min_val (float): Minimum value for normalization.
            max_val (float): Maximum value for normalization.
            size (int): Size of the target axis (width or height).

        Returns:
            np.ndarray: Normalized image coordinates.
        """
        return (values - min_val) / (max_val - min_val) * (size - 1)

    def latlon_to_image_coords(
        self, lat: np.ndarray, lon: np.ndarray, shape: Tuple[int, int]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert latitude and longitude to Gnomonic image coordinates.

        Args:
            lat (np.ndarray): Latitude values in degrees.
            lon (np.ndarray): Longitude values in degrees.
            shape (Tuple[int, int]): Shape of the target image (height, width).

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y coordinates in image space.

        Raises:
            TransformationError: If input arrays are invalid or computation fails.
            ConfigurationError: If config lacks required attributes.
        """
        logger.debug("Transforming latitude and longitude to image coordinates.")
        try:
            self._validate_inputs(lat, "lat")
            self._validate_inputs(lon, "lon")
            H, W = shape[:2]
            logger.debug(f"Image shape received: H={H}, W={W}")

            # Compute normalized image coordinates based on geographic bounds
            map_x = self._compute_image_coords(
                lon, self.config.lon_min, self.config.lon_max, W
            )
            map_y = self._compute_image_coords(
                lat, self.config.lat_max, self.config.lat_min, H
            )
            logger.debug("Computed image coordinates successfully.")
            return map_x, map_y
        except Exception as e:
            logger.exception("Failed to transform latitude and longitude to image coordinates.")
            raise TransformationError(f"Gnomonic lat/lon transformation failed: {e}")

    def xy_to_image_coords(
        self, x: np.ndarray, y: np.ndarray, config: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Transform XY grid coordinates to image coordinates.

        Args:
            x (np.ndarray): X grid coordinates in planar space.
            y (np.ndarray): Y grid coordinates in planar space.
            config (Any): Configuration object containing projection parameters.

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y coordinates in image space.

        Raises:
            TransformationError: If input arrays are invalid or computation fails.
        """
        logger.debug("Transforming XY grid coordinates to image coordinates.")
        try:
            self._validate_inputs(x, "x")
            self._validate_inputs(y, "y")

            # Compute grid bounds based on field of view and Earth's radius
            half_fov_rad = np.deg2rad(config.fov_deg / 2)
            x_max = np.tan(half_fov_rad) * config.R
            y_max = np.tan(half_fov_rad) * config.R
            x_min, y_min = -x_max, -y_max
            logger.debug(f"Computed grid bounds: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")

            # Transform grid coordinates to normalized image coordinates
            map_x = self._compute_image_coords(x, x_min, x_max, config.x_points)
            map_y = self._compute_image_coords(y, y_max, y_min, config.y_points)
            logger.debug("Grid coordinates transformed to image coordinates successfully.")
            return map_x, map_y
        except Exception as e:
            logger.exception("Failed to transform XY grid coordinates to image coordinates.")
            raise TransformationError(f"Gnomonic XY transformation failed: {e}")