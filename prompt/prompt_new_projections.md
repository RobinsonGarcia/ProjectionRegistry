Below is a step-by-step guide to implement a new projection type in your Python package. These instructions reference the Gnomonic projection implementation as a guiding example. The key requirement is that your new projection must define four primary components:
	1.	Configuration (config.py): Defines and validates user-facing parameters (e.g., radius, lat/lon bounds).
	2.	Grid Generation (grid.py): Produces forward and backward grids (e.g., projection grids vs. spherical grids).
	3.	Projection Strategy (strategy.py): Encodes the forward and inverse mapping math between spherical (lat/lon) and planar coordinates.
	4.	Coordinate Transform (transform.py): Converts between (lat/lon or x/y) and final image coordinates.

Finally, you must register your new projection in the ProjectionRegistry. Below, each numbered section outlines how to implement and wire up these components.

# 1. Create Your Projection Folder and Files

Start by creating a new folder under projection/ with the name of your new projection (e.g., projection/my_projection/):

```python
projection/
    ...
    my_projection/
        __init__.py
        config.py
        grid.py
        strategy.py
        transform.py

```

# 2. Implement the Configuration (config.py)

Your new configuration file should contain two main pieces:
	1.	A Pydantic model class that defines and validates the parameters for your projection.
	2.	A configuration-wrapper class that can be used by the rest of the system (particularly BaseProjectionConfig).

Below is a minimal structure, taking gnomonic/config.py as an example.

```python
# my_projection/config.py

import logging
from typing import Any, Optional
from pydantic import BaseModel, Field, validator
import cv2

from ..exceptions import ConfigurationError

logger = logging.getLogger("projection.my_projection.config")

class MyProjectionConfigModel(BaseModel):
    """
    Pydantic model for MyProjection projection configuration.
    Define all the parameters your projection needs:
      - R (radius)
      - center latitude, center longitude
      - bounding box for lat/lon
      - resolution
      - interpolation settings
      - etc.
    """
    R: float = Field(6371.0, description="Radius of the Earth (or sphere) in kilometers.")
    phi0_deg: float = Field(0.0, description="Latitude center in degrees.")
    lam0_deg: float = Field(0.0, description="Longitude center in degrees.")
    # Add as many fields as required by your math...
    
    x_points: int = Field(512, description="Number of points in x-direction.")
    y_points: int = Field(512, description="Number of points in y-direction.")
    
    lon_min: float = Field(-180.0, description="Min longitude for grid.")
    lon_max: float = Field(180.0, description="Max longitude for grid.")
    lat_min: float = Field(-90.0, description="Min latitude for grid.")
    lat_max: float = Field(90.0, description="Max latitude for grid.")
    
    interpolation: Optional[int] = Field(default=cv2.INTER_LINEAR, description="OpenCV interpolation mode.")
    borderMode: Optional[int] = Field(default=cv2.BORDER_CONSTANT, description="OpenCV border mode.")
    borderValue: Optional[Any] = Field(default=0, description="OpenCV border value.")

    @validator("R")
    def validate_radius(cls, v):
        if v <= 0:
            raise ValueError("Sphere/Earth radius must be > 0.")
        return v

class MyProjectionConfig:
    """
    Wrapper for MyProjectionConfigModel to be used by the rest of the system.
    Mirrors the design of GnomonicConfig, MercatorConfig, etc.
    """

    def __init__(self, **kwargs: Any) -> None:
        logger.debug("Initializing MyProjectionConfig with parameters: %s", kwargs)
        try:
            self.config = MyProjectionConfigModel(**kwargs)
            logger.info("MyProjectionConfig initialized successfully.")
        except Exception as e:
            error_msg = f"Failed to initialize MyProjectionConfig: {e}"
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from e

    def update(self, **kwargs: Any) -> None:
        """
        Dynamically update the projection parameters.
        """
        logger.debug(f"Updating MyProjectionConfig with parameters: {kwargs}")
        try:
            updated_config = self.config.copy(update=kwargs)
            self.config = updated_config
            logger.info("MyProjectionConfig updated successfully.")
        except Exception as e:
            error_msg = f"Failed to update MyProjectionConfig: {e}"
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from e

    def __getattr__(self, item: str) -> Any:
        """
        Access the pydantic config fields as attributes.
        """
        logger.debug(f"Accessing MyProjectionConfig attribute '{item}'.")
        try:
            return getattr(self.config, item)
        except AttributeError:
            error_msg = f"'MyProjectionConfig' object has no attribute '{item}'"
            logger.error(error_msg)
            raise AttributeError(error_msg)

    def __repr__(self) -> str:
        """
        String representation for debugging/logging.
        """
        return f"MyProjectionConfig({self.config.dict()})"

```
Key points for config:
	•	Subclass BaseModel for strong validation and documentation.
	•	Provide a simple wrapper class (like MyProjectionConfig) that will be used by the registry and the BaseProjectionConfig logic.


# 3. Implement the Grid Generation (grid.py)

Your new projection’s grid module must extend BaseGridGeneration and implement two main methods:
	1.	projection_grid(): Usually returns (X, Y) arrays for forward projection.
	2.	spherical_grid(): Usually returns (lon, lat) arrays for backward projection.

Using gnomonic/grid.py as a pattern:

```python
# my_projection/grid.py

import logging
import numpy as np
from typing import Tuple
from ..base.grid import BaseGridGeneration
from ..exceptions import GridGenerationError

logger = logging.getLogger("projection.my_projection.grid")

class MyProjectionGridGeneration(BaseGridGeneration):
    """
    Generates forward and backward grids for MyProjection.
    """

    def projection_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create the planar (X, Y) grid for forward projection.
        """
        logger.debug("Generating MyProjection forward grid.")
        try:
            # Example: use the field-of-view or bounding box from the config
            # to define the extent of x, y
            R = self.config.R
            x_vals = np.linspace(-R, R, self.config.x_points)
            y_vals = np.linspace(-R, R, self.config.y_points)
            grid_x, grid_y = np.meshgrid(x_vals, y_vals)
            return grid_x, grid_y
        except Exception as e:
            error_msg = f"Failed to generate forward grid: {e}"
            logger.exception(error_msg)
            raise GridGenerationError(error_msg)

    def spherical_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create the (lon, lat) grid for backward projection.
        """
        logger.debug("Generating MyProjection spherical grid.")
        try:
            lon_vals = np.linspace(self.config.lon_min, self.config.lon_max, self.config.x_points)
            lat_vals = np.linspace(self.config.lat_min, self.config.lat_max, self.config.y_points)
            grid_lon, grid_lat = np.meshgrid(lon_vals, lat_vals)
            return grid_lon, grid_lat
        except Exception as e:
            error_msg = f"Failed to generate spherical grid: {e}"
            logger.exception(error_msg)
            raise GridGenerationError(error_msg)

```
Key points for grid:
	•	Extend BaseGridGeneration.
	•	Implement projection_grid() and spherical_grid() to return np.ndarray meshes.
	•	Use your config parameters (e.g., self.config.x_points, self.config.y_points, bounding box, etc.).

# 4. Implement the Projection Strategy (strategy.py)

Your projection strategy does the actual math mapping from (\text{lat}, \text{lon}) to (x,y) and back again. It should:
	•	Extend BaseProjectionStrategy.
	•	Implement:
	1.	from_spherical_to_projection(lat, lon) -> (x, y, mask)
	2.	from_projection_to_spherical(x, y) -> (lat, lon)

As with gnomonic/strategy.py:

```python
# my_projection/strategy.py

import logging
import numpy as np
from typing import Tuple
from ..base.strategy import BaseProjectionStrategy
from ..exceptions import ProcessingError
from .config import MyProjectionConfig

logger = logging.getLogger("projection.my_projection.strategy")

class MyProjectionStrategy(BaseProjectionStrategy):
    """
    Implements forward (lat/lon -> x/y) and inverse (x/y -> lat/lon)
    transformations for MyProjection.
    """

    def __init__(self, config: MyProjectionConfig) -> None:
        """
        Initialize with validated config. 
        """
        logger.debug("Initializing MyProjectionStrategy.")
        if not isinstance(config, MyProjectionConfig):
            error_msg = f"config must be MyProjectionConfig, got {type(config)}"
            logger.error(error_msg)
            raise TypeError(error_msg)
        self.config = config
        logger.info("MyProjectionStrategy initialized successfully.")

    def from_spherical_to_projection(
        self, lat: np.ndarray, lon: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Forward: lat/lon (degrees) -> x/y (units).
        Return (x, y, mask).
        """
        logger.debug("Starting forward MyProjection transformation.")
        try:
            # Convert degrees to radians if needed
            lat_rad = np.radians(lat)
            lon_rad = np.radians(lon)

            # Insert your projection’s forward math here:
            # For example, x = R * ...
            #              y = R * ...
            x = self.config.R * (lon_rad - np.radians(self.config.lam0_deg))
            y = self.config.R * (lat_rad - np.radians(self.config.phi0_deg))

            # mask can identify valid/invalid regions of your projection
            mask = np.ones_like(x, dtype=bool)
            return x, y, mask
        except Exception as e:
            error_msg = f"Forward MyProjection error: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg)

    def from_projection_to_spherical(
        self, x: np.ndarray, y: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Inverse: x/y -> lat/lon (degrees).
        """
        logger.debug("Starting inverse MyProjection transformation.")
        try:
            lat_rad = (y / self.config.R) + np.radians(self.config.phi0_deg)
            lon_rad = (x / self.config.R) + np.radians(self.config.lam0_deg)

            lat = np.degrees(lat_rad)
            lon = np.degrees(lon_rad)
            return lat, lon
        except Exception as e:
            error_msg = f"Inverse MyProjection error: {e}"
            logger.exception(error_msg)
            raise ProcessingError(error_msg)
```
Key points for strategy:
	•	Make sure your forward method returns (x, y, mask); mask helps identify out-of-bounds or invalid points.
	•	Properly handle degrees ↔ radians.
	•	Raise ProcessingError (or relevant exceptions) if something goes wrong.

# 5. Implement the Coordinate Transformer (transform.py)

The transform class extends BaseCoordinateTransformer. It typically has two methods:
	1.	spherical_to_image_coords(lat, lon, shape) -> (map_x, map_y): Convert lat/lon to pixel coordinates.
	2.	projection_to_image_coords(x, y, config) -> (map_x, map_y): Convert projection-plane (x, y) to pixel coordinates.

See gnomonic/transform.py for how Gnomonic uses fov_deg and the radius to derive pixel scaling. A simple example:
```python
# my_projection/transform.py

import logging
import numpy as np
from typing import Tuple, Any
from ..base.transform import BaseCoordinateTransformer
from ..exceptions import TransformationError, ConfigurationError

logger = logging.getLogger("projection.my_projection.transform")

class MyProjectionTransformer(BaseCoordinateTransformer):
    """
    Convert lat/lon or x/y in MyProjection to final image pixel coords.
    """

    def __init__(self, config: Any):
        super().__init__(config)
        logger.debug("Initializing MyProjectionTransformer.")
        # Validate needed attributes
        required = ["lon_min", "lon_max", "lat_min", "lat_max", "x_points", "y_points"]
        missing = [attr for attr in required if not hasattr(config, attr)]
        if missing:
            error_msg = f"Config missing attributes: {', '.join(missing)}"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
        logger.info("MyProjectionTransformer initialized successfully.")

    def spherical_to_image_coords(
        self, lat: np.ndarray, lon: np.ndarray, shape: Tuple[int, int]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert lat/lon (degrees) to image pixel indices.
        shape is typically (height, width) of the input image.
        """
        logger.debug("Starting MyProjection spherical_to_image_coords.")
        H, W = shape

        # Basic example of linear scaling:
        map_x = (lon - self.config.lon_min) / (self.config.lon_max - self.config.lon_min) * (W - 1)
        map_y = (self.config.lat_max - lat) / (self.config.lat_max - self.config.lat_min) * (H - 1)
        
        return map_x, map_y

    def projection_to_image_coords(
        self, x: np.ndarray, y: np.ndarray, config: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert MyProjection x/y to image coords, e.g. scaling from ±some range into [0, width-1].
        """
        logger.debug("Starting MyProjection projection_to_image_coords.")
        # Suppose we define the domain from -max_extent to +max_extent, etc.
        max_extent = self.config.R  # or compute from fov_deg if relevant
        min_extent = -max_extent

        map_x = ((x - min_extent) / (max_extent - min_extent)) * (self.config.x_points - 1)
        map_y = ((max_extent - y) / (max_extent - min_extent)) * (self.config.y_points - 1)

        return map_x, map_y
```
Key points for transform:
	•	Subclass BaseCoordinateTransformer.
	•	Validate config attributes in __init__.
	•	Provide meaningful scaling from your (x, y) or (\text{lat}, \text{lon}) domain into pixel image coordinates.

# # default_projections.py (or wherever you prefer)
from .registry import ProjectionRegistry

# Import your classes
from .my_projection.config import MyProjectionConfig
from .my_projection.grid import MyProjectionGridGeneration
from .my_projection.strategy import MyProjectionStrategy
from .my_projection.transform import MyProjectionTransformer

# Possibly your custom interpolation class, or just use BaseInterpolation
from .base.interpolation import BaseInterpolation

def register_default_projections():
    ...
    # Register your new projection
    ProjectionRegistry.register("my_projection", {
        "config": MyProjectionConfig,
        "grid_generation": MyProjectionGridGeneration,
        "projection_strategy": MyProjectionStrategy,
        "interpolation": BaseInterpolation,           # or your own
        "transformer": MyProjectionTransformer,       # or your own
    })
    ...

# 7. Verify Your Implementation
	1.	Check config: Instantiate MyProjectionConfig(...) with various parameters. Confirm validation works.
	2.	Check grid: Instantiate MyProjectionGridGeneration(config).projection_grid() and spherical_grid()—check shapes and expected numeric ranges.
	3.	Check strategy: Confirm your math in from_spherical_to_projection() and from_projection_to_spherical() with known test points.
	4.	Check transform: Ensure spherical_to_image_coords() and projection_to_image_coords() produce the pixel coordinates you expect.
	5.	Perform a test projection:

```python
processor = ProjectionRegistry.get_projection("my_projection", return_processor=True, R=8000.0)
forward_img = processor.forward(input_img)
back_img = processor.backward(forward_img)
```
Summary of the Required Steps
	1.	Create my_projection/config.py:
	•	A Pydantic model MyProjectionConfigModel.
	•	A wrapper class MyProjectionConfig.
	2.	Create my_projection/grid.py:
	•	Extend BaseGridGeneration.
	•	Implement projection_grid() (forward grid) and spherical_grid() (backward grid).
	3.	Create my_projection/strategy.py:
	•	Extend BaseProjectionStrategy.
	•	Implement the forward (from_spherical_to_projection) and inverse (from_projection_to_spherical) projection logic.
	4.	Create my_projection/transform.py:
	•	Extend BaseCoordinateTransformer.
	•	Implement methods to convert lat/lon → image coords and x/y → image coords.
	5.	Register your projection via ProjectionRegistry.register(...).
	6.	Use your new projection by retrieving a processor or config from the registry.

By following these guidelines (mirroring the structure of the Gnomonic implementation), you will have a fully functional, registerable projection integrated into your package. Good luck implementing your new projection type!
