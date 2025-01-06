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
        H, W = shape  # Extract image height and width
 
        lon[lon>180] = 180 - lon[lon>180]
        lat[lat>90] = 90 - lat[lat>90]
        map_x = self._compute_image_coords(
            lon, self.config.lon_min, self.config.lon_max, W
        )
        map_y = self._compute_image_coords(
            lat, self.config.lat_max, self.config.lat_min, H
        )
        return map_x, map_y


    def projection_to_image_coords(
        self, x: np.ndarray, y: np.ndarray, config: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
    
        half_fov_rad = np.deg2rad(config.fov_deg / 2)  # Convert half FOV to radians
        x_max = np.tan(half_fov_rad) * config.R          # Maximum X value based on FOV
        y_max = np.tan(half_fov_rad) * config.R          # Maximum Y value based on FOV
        x_min, y_min = -x_max, -y_max                    # Define minimum X and Y values

        # Normalize planar X coordinates to image width based on grid bounds
        map_x = self._compute_image_coords(x, x_min, x_max, config.x_points)

        # Normalize planar Y coordinates to image height based on grid bounds
        # Note: Y coordinates are typically mapped from top (y_max) to bottom (y_min)
        map_y = self._compute_image_coords(y, y_max, y_min, config.y_points)

        return map_x, map_y
