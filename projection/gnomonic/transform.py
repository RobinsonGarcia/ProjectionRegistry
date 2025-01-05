from typing import Tuple, Any
import numpy as np
import logging
from ..exceptions import TransformationError, ConfigurationError
from ..base.transform import BaseCoordinateTransformer
# Configure logger for the transformation module
logger = logging.getLogger('gnomonic_projection.gnomonic.transform')

class GnomonicTransformer(BaseCoordinateTransformer):
    """
    Transformation Logic for Gnomonic Projection.

    The `GnomonicTransformer` class handles the conversion between geographic coordinates
    (latitude and longitude) and image coordinates on the Gnomonic projection plane. This conversion
    is essential for preparing data before performing image interpolation, ensuring accurate mapping
    between different projection systems.

    ## Transformation Methods:

    - **latlon_to_image_coords:** Converts geographic coordinates from an equirectangular image to image coordinates.
    - **xy_to_image_coords:** Converts planar grid coordinates from the Gnomonic projection to image coordinates.
    """

    def __init__(self, config):
        """
        Initialize the GnomonicTransformer with the given configuration.

        This initializer validates the provided configuration object to ensure that all
        necessary attributes are present. It raises a ConfigurationError if any required
        attribute is missing, preventing the transformer from operating with incomplete
        or incorrect configurations.

        Args:
            config: Configuration object containing necessary projection parameters.

        Raises:
            ConfigurationError: If the configuration object lacks required attributes.
        """
        # Define the required attributes for the configuration
        required_attributes = [
            "lon_min",    # Minimum longitude value
            "lon_max",    # Maximum longitude value
            "lat_min",    # Minimum latitude value
            "lat_max",    # Maximum latitude value
            "fov_deg",    # Field of view in degrees
            "R",          # Radius of the Earth or sphere being projected
            "x_points",   # Number of points along the X-axis (width)
            "y_points"    # Number of points along the Y-axis (height)
        ]
        # Check for any missing attributes in the configuration
        missing_attributes = [attr for attr in required_attributes if not hasattr(config, attr)]

        if missing_attributes:
            # Log an error if any required attribute is missing
            error_msg = f"Configuration object is missing required attributes: {', '.join(missing_attributes)}"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)

        # Store the validated configuration object for use in other methods
        self.config = config
        logger.info("GnomonicTransformer initialized successfully.")

    def _validate_inputs(self, array: np.ndarray, name: str) -> None:
        """
        Validate input arrays to ensure they are NumPy arrays.

        This helper method checks whether the provided input is an instance of NumPy's ndarray.
        It raises a TransformationError if the input is not valid, ensuring that subsequent
        computations operate on the correct data types.

        Args:
            array (np.ndarray): Input array to validate.
            name (str): Name of the array for error messages.

        Raises:
            TransformationError: If the input is invalid (i.e., not a NumPy ndarray).
        """
        if not isinstance(array, np.ndarray):
            # Log an error if the input is not a NumPy ndarray
            error_msg = f"{name} must be a NumPy ndarray."
            logger.error(error_msg)
            raise TransformationError(error_msg)

    def _compute_image_coords(
        self, values: np.ndarray, min_val: float, max_val: float, size: int
    ) -> np.ndarray:
        """
        Generalized method to compute normalized image coordinates.

        This method normalizes input values (such as latitude, longitude, x, or y)
        to fit within the dimensions of the target image. The normalization scales
        the values to the range [0, size-1], where `size` corresponds to the width
        or height of the image axis.

        Args:
            values (np.ndarray): Input values to normalize (e.g., latitudes, longitudes, x, y).
            min_val (float): Minimum value for normalization.
            max_val (float): Maximum value for normalization.
            size (int): Size of the target axis (width or height of the image).

        Returns:
            np.ndarray: Normalized image coordinates scaled to [0, size-1].
        """
        # Perform normalization of the input values
        normalized = (values - min_val) / (max_val - min_val) * (size - 1)
        logger.debug(f"Computed normalized image coordinates: {normalized}")
        return normalized

    def spherical_to_image_coords(
        self, lat: np.ndarray, lon: np.ndarray, shape: Tuple[int, int]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert geographic coordinates (latitude and longitude) to image coordinates.

        This method maps the geographic coordinates from an equirectangular (input) image
        to planar grid coordinates on the Gnomonic projection plane. The resulting image
        coordinates (`map_x`, `map_y`) are essential for interpolating the input image
        onto the projection plane accurately.

        Args:
            lat (np.ndarray): Latitude values in degrees.
            lon (np.ndarray): Longitude values in degrees.
            shape (Tuple[int, int]): Shape of the target image as (height, width).

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y coordinates in image space suitable for interpolation.

        Raises:
            TransformationError: If input arrays are invalid or if computation fails.
            ConfigurationError: If the configuration lacks required attributes.
        """
        logger.debug("Transforming geographic coordinates (lat/lon) to image coordinates.")
        try:
            # Validate that latitude and longitude inputs are NumPy arrays
            self._validate_inputs(lat, "lat")
            self._validate_inputs(lon, "lon")
            H, W = shape  # Extract image height and width
            logger.debug(f"Target image shape: Height={H}, Width={W}")

            # Normalize longitude to the image width based on geographic bounds
            map_x = self._compute_image_coords(
                lon, self.config.lon_min, self.config.lon_max, W
            )
            logger.debug("Normalized longitude to image X coordinates.")

            # Normalize latitude to the image height based on geographic bounds
            # Note: Latitude is typically mapped from top (max_lat) to bottom (min_lat)
            map_y = self._compute_image_coords(
                lat, self.config.lat_max, self.config.lat_min, H
            )
            logger.debug("Normalized latitude to image Y coordinates.")

            logger.debug("Latitude and longitude transformed successfully.")
            return map_x, map_y
        except Exception as e:
            # Log the exception with traceback and raise a TransformationError
            logger.exception("Failed to transform latitude and longitude to image coordinates.")
            raise TransformationError(f"Gnomonic lat/lon transformation failed: {e}")

    def projection_to_image_coords(
        self, x: np.ndarray, y: np.ndarray, config: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Transform planar grid coordinates (x, y) to image coordinates.

        This method maps the planar grid coordinates from the Gnomonic projection plane
        to corresponding image coordinates in the output equirectangular image. The resulting
        image coordinates (`map_x`, `map_y`) are used for interpolating the projected image
        back to an equirectangular format.

        Args:
            x (np.ndarray): X grid coordinates in planar space.
            y (np.ndarray): Y grid coordinates in planar space.
            config (Any): Configuration object containing projection parameters.

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y coordinates in image space suitable for interpolation.

        Raises:
            TransformationError: If input arrays are invalid or if computation fails.
        """
        logger.debug("Transforming planar grid coordinates (x/y) to image coordinates.")
        try:
            # Validate that x and y inputs are NumPy arrays
            self._validate_inputs(x, "x")
            self._validate_inputs(y, "y")

            # Compute grid bounds based on field of view and Earth's radius
            half_fov_rad = np.deg2rad(config.fov_deg / 2)  # Convert half FOV to radians
            x_max = np.tan(half_fov_rad) * config.R          # Maximum X value based on FOV
            y_max = np.tan(half_fov_rad) * config.R          # Maximum Y value based on FOV
            x_min, y_min = -x_max, -y_max                    # Define minimum X and Y values
            logger.debug(f"Computed grid bounds: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")

            # Normalize planar X coordinates to image width based on grid bounds
            map_x = self._compute_image_coords(x, x_min, x_max, config.x_points)
            logger.debug("Normalized planar X to image coordinates.")

            # Normalize planar Y coordinates to image height based on grid bounds
            # Note: Y coordinates are typically mapped from top (y_max) to bottom (y_min)
            map_y = self._compute_image_coords(y, y_max, y_min, config.y_points)
            logger.debug("Normalized planar Y to image coordinates.")

            logger.debug("Planar grid coordinates transformed successfully.")
            return map_x, map_y
        except Exception as e:
            # Log the exception with traceback and raise a TransformationError
            logger.exception("Failed to transform XY grid coordinates to image coordinates.")
            raise TransformationError(f"Gnomonic XY transformation failed: {e}")