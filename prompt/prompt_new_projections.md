Below is a step-by-step guide on how to create and integrate a new projection into this framework, similar to how **gnomonic** and **mercator** projections were added. The explanation covers both conceptual and implementation details. By following these steps, you’ll end up with a fully functional forward (equirectangular → your projection) and backward (your projection → equirectangular) transformation pipeline.

---

## 1. **Conceptual Overview**

1. **Equirectangular (Spherical) Space**  
   - We use equirectangular images as the “sphere” representation.  
   - In an equirectangular image, the x-axis corresponds to longitude (typically \(-180^\circ\) to \(+180^\circ\)) and the y-axis corresponds to latitude (\(+90^\circ\) to \(-90^\circ\)).

2. **Forward Method** (`processor.forward(img)`)  
   - **Goal**: Transform from spherical (equirectangular) coordinates to your new projection’s coordinates.  
   - **Steps**:  
     a. Generate a **projection grid** \((x, y)\) in your new projection’s coordinate system.  
     b. Convert that \((x, y)\) to \((\text{lat}, \text{lon})\) using your projection’s **inverse** equations (a.k.a. `_from_projection_to_spherical`).  
     c. Map lat/lon onto the input equirectangular image by computing the appropriate (map_x, map_y) in equirectangular space.  
     d. Interpolate the pixels from the original image to produce the final forward-projected image.

3. **Backward Method** (`processor.backward(img)`)  
   - **Goal**: Transform from your new projection’s coordinates back to spherical (equirectangular).  
   - **Steps**:  
     a. Generate a **spherical grid** \((\text{lon}, \text{lat})\).  
     b. Convert that \((\text{lat}, \text{lon})\) to the projection coordinate system \((x, y)\) using your projection’s **forward** equations (a.k.a. `_from_spherical_to_projection`).  
     c. Map \((x, y)\) into the coordinate space of the input “rectilinear” image using `projection_to_image_coords`, then interpolate.

4. **Classes Involved**  
   - **`BaseProjectionConfig`**: Holds parameters such as `lon_min`, `lon_max`, `lat_min`, `lat_max`, `fov_deg`, `x_points`, `y_points`, interpolation options, etc.  
   - **`BaseGridGeneration`**: Generates the coordinate grids needed for forward/backward transformations.  
   - **`BaseProjectionStrategy`**: Implements the core forward (`_from_spherical_to_projection`) and inverse (`_from_projection_to_spherical`) mathematical logic.  
   - **`BaseCoordinateTransformer`**: Handles the mapping of lat/lon or (x, y) to image pixel coordinates.  
   - **`BaseInterpolation`**: Performs the actual image remapping (e.g., via OpenCV).

5. **Registry & Processor**  
   - **`ProjectionRegistry`**: A central place that knows about all projections. Each projection is “registered” here.  
   - **`ProjectionProcessor`**: Uses the configuration, grid generation, projection strategy, transformer, and interpolation to run the forward/backward pipelines in one high-level call (`processor.forward(...)` or `processor.backward(...)`).

---

## 2. **Directory and File Setup**

Following the pattern for `gnomonic/` and `mercator/`, create a new folder for your projection, for example, **`my_projection/`**:


projection/
   ...
   ├── my_projection/
   │   ├── __init__.py
   │   ├── config.py
   │   ├── grid.py
   │   ├── strategy.py
   │   └── transform.py
   ...


### 2.1 `__init__.py`
Inside `my_projection/__init__.py`, you can optionally expose only the classes you want to be publicly visible. For instance:

```python
from .config import MyProjectionConfig
from .grid import MyProjectionGridGeneration
from .strategy import MyProjectionStrategy
from .transform import MyProjectionTransformer

__all__ = [
    "MyProjectionConfig",
    "MyProjectionGridGeneration",
    "MyProjectionStrategy",
    "MyProjectionTransformer",
]
```

## 3. Create a Config Class (config.py)

Your configuration class should hold and validate parameters needed for your projection. It usually follows this structure:
	1.	A Pydantic model (e.g., MyProjectionConfigModel) describing your settings.
	2.	A Python class (e.g., MyProjectionConfig) that wraps the model and implements methods like update for dynamic reconfiguration.

Example:

```python
# my_projection/config.py
from typing import Any, Optional
from pydantic import BaseModel, Field, validator
import cv2
import logging
from ..exceptions import ConfigurationError

logger = logging.getLogger('my_projection.config')

class MyProjectionConfigModel(BaseModel):
    # Example fields; adjust for your math
    R: float = Field(6371.0, description="Planet radius.")
    center_lat: float = Field(0.0, description="Center latitude for the projection.")
    center_lon: float = Field(0.0, description="Center longitude for the projection.")
    # Possibly a field-of-view, or other domain-specific parameters
    fov_deg: float = Field(90.0, description="Field of view in degrees.")
    x_points: int = Field(512, description="Resolution in x-direction.")
    y_points: int = Field(512, description="Resolution in y-direction.")
    lon_min: float = Field(-180.0, description="Minimum longitude in equirectangular space.")
    lon_max: float = Field(180.0, description="Maximum longitude in equirectangular space.")
    lat_min: float = Field(-90.0, description="Minimum latitude in equirectangular space.")
    lat_max: float = Field(90.0, description="Maximum latitude in equirectangular space.")
    interpolation: Optional[int] = Field(default=cv2.INTER_LINEAR, description="OpenCV interpolation mode.")
    borderMode: Optional[int] = Field(default=cv2.BORDER_CONSTANT, description="OpenCV border mode.")
    borderValue: Optional[Any] = Field(default=0, description="OpenCV border value.")

    @validator('fov_deg')
    def validate_fov(cls, v):
        if not (0 < v < 180):
            raise ValueError("Field of view (fov_deg) must be >0 and <180.")
        return v

    class Config:
        arbitrary_types_allowed = True

class MyProjectionConfig:
    def __init__(self, **kwargs: Any):
        logger.debug("Initializing MyProjectionConfig with parameters: %s", kwargs)
        try:
            self.config = MyProjectionConfigModel(**kwargs)
            logger.info("MyProjectionConfig initialized successfully.")
        except Exception as e:
            error_msg = f"Failed to initialize MyProjectionConfig: {e}"
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from e

    def update(self, **kwargs: Any) -> None:
        logger.debug(f"Updating MyProjectionConfig with parameters: {kwargs}")
        try:
            updated = self.config.copy(update=kwargs)
            self.config = updated
        except Exception as e:
            error_msg = f"Failed to update MyProjectionConfig: {e}"
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from e

    def __getattr__(self, item: str) -> Any:
        try:
            return getattr(self.config, item)
        except AttributeError:
            error_msg = f"'MyProjectionConfig' object has no attribute '{item}'"
            logger.error(error_msg)
            raise AttributeError(error_msg)

    def __repr__(self) -> str:
        return f"MyProjectionConfig({self.config.dict()})"
```

## 4. Create a Grid Generation Class (grid.py)

Your projection may require a custom approach to generate the forward “projection grid” and the backward “spherical grid.” For instance:

```python
# my_projection/grid.py
import numpy as np
import logging
from typing import Tuple
from ..base.grid import BaseGridGeneration

logger = logging.getLogger('my_projection.grid')

class MyProjectionGridGeneration(BaseGridGeneration):
    def _projection_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate a (x_grid, y_grid) for forward projection.
        - Typically covers the extent you plan to project.
        """
        half_fov_rad = np.deg2rad(self.config.fov_deg / 2)
        # Example: Extent in X/Y = R * tan(FOV/2)
        x_extent = np.tan(half_fov_rad) * self.config.R
        y_extent = np.tan(half_fov_rad) * self.config.R

        x_vals = np.linspace(-x_extent, x_extent, self.config.x_points)
        y_vals = np.linspace(-y_extent, y_extent, self.config.y_points)
        grid_x, grid_y = np.meshgrid(x_vals, y_vals)

        return grid_x, grid_y

    def _spherical_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate a (lon_grid, lat_grid) for backward projection.
        """
        lon_vals = np.linspace(self.config.lon_min, self.config.lon_max, self.config.x_points)
        lat_vals = np.linspace(self.config.lat_min, self.config.lat_max, self.config.y_points)
        grid_lon, grid_lat = np.meshgrid(lon_vals, lat_vals)

        return grid_lon, grid_lat
```
## 5. Create a Strategy Class (strategy.py)

This is where your forward (lat/lon → x/y) and inverse (x/y → lat/lon) formulas live. You will inherit from BaseProjectionStrategy and implement:
	•	\_from_spherical_to_projection(...): The forward math
	•	\_from_projection_to_spherical(...): The inverse math
```python
# my_projection/strategy.py
import numpy as np
import logging
from ..base.strategy import BaseProjectionStrategy

logger = logging.getLogger('my_projection.strategy')

class MyProjectionStrategy(BaseProjectionStrategy):
    def _from_spherical_to_projection(self, lat: np.ndarray, lon: np.ndarray):
        """
        Forward: (lat, lon) --> (x, y).
        Return (x, y, mask).
        - mask can help filter out invalid regions if cos_c <= 0, etc.
        """
        # Convert degrees to radians
        center_lat_rad = np.deg2rad(self.config.center_lat)
        center_lon_rad = np.deg2rad(self.config.center_lon)
        lat_rad = np.deg2rad(lat)
        lon_rad = np.deg2rad(lon)

        # Insert your forward equations here.
        # Example pseudo-code (this is NOT a real formula):
        x = self.config.R * (lon_rad - center_lon_rad)
        y = self.config.R * (lat_rad - center_lat_rad)

        # Create a boolean mask to indicate valid/invalid projection points
        mask = np.ones_like(x, dtype=bool)
        return x, y, mask

    def _from_projection_to_spherical(self, x: np.ndarray, y: np.ndarray):
        """
        Inverse: (x, y) --> (lat, lon).
        """
        center_lat_rad = np.deg2rad(self.config.center_lat)
        center_lon_rad = np.deg2rad(self.config.center_lon)

        lat_rad = (y / self.config.R) + center_lat_rad
        lon_rad = (x / self.config.R) + center_lon_rad

        lat = np.rad2deg(lat_rad)
        lon = np.rad2deg(lon_rad)
        return lat, lon

```
## 6. Create a Transformer Class (transform.py)

The transformer handles how ((\text{lat}, \text{lon})) or ((x, y)) get mapped to pixel coordinates in an image. Typically:
	•	spherical_to_image_coords(lat, lon, shape): Maps lat/lon to pixel ((map_x, map_y)) for the input equirectangular image dimensions.
	•	projection_to_image_coords(x, y, shape): Maps your new projection’s ((x, y)) to pixel ((map_x, map_y)) if needed.

```python
# my_projection/transform.py
from ..base.transform import BaseCoordinateTransformer
import numpy as np
import logging

logger = logging.getLogger('my_projection.transform')

class MyProjectionTransformer(BaseCoordinateTransformer):
    def _spherical_to_image_coords(self, lat: np.ndarray, lon: np.ndarray, shape: tuple):
        self._validate_inputs(lat, "lat")
        self._validate_inputs(lon, "lon")
        
        H, W = shape[:2]  # image height, width
        # Map lon from [lon_min, lon_max] to [0, W-1]
        map_x = (lon - self.config.lon_min) / (self.config.lon_max - self.config.lon_min) * (W - 1)
        # Map lat from [lat_max, lat_min] inversely down the image
        map_y = (self.config.lat_max - lat) / (self.config.lat_max - self.config.lat_min) * (H - 1)

        return map_x, map_y

    def _projection_to_image_coords(self, x: np.ndarray, y: np.ndarray, shape: tuple):
        self._validate_inputs(x, "x")
        self._validate_inputs(y, "y")

        # For forward-projection images, you might map the (x, y) from [-extent, extent]
        # to [0, width-1 / height-1].
        # Example:
        half_fov_rad = np.deg2rad(self.config.fov_deg / 2)
        max_val = np.tan(half_fov_rad) * self.config.R
        min_val = -max_val

        W, H = self.config.x_points, self.config.y_points
        # Normalize x
        map_x = (x - min_val) / (max_val - min_val) * (W - 1)
        # Normalize y (top->bottom)
        map_y = (max_val - y) / (max_val - min_val) * (H - 1)

        return map_x, map_y
```
(You can adapt these formulas based on how you want to interpret the grids in your new projection. The main idea is that each dimension in your projection gets normalized to pixel indices.)

7. Register Your Projection (default_projections.py or Similar)
	1.	Import your newly created classes into default_projections.py (or wherever you handle the “official” registry addition).
	2.	Call ProjectionRegistry.register("my_projection", {...}) with the required components.

Example:
```python
# default_projections.py

from .registry import ProjectionRegistry

# Import from your new folder
from .my_projection.config import MyProjectionConfig
from .my_projection.grid import MyProjectionGridGeneration
from .my_projection.strategy import MyProjectionStrategy
from .my_projection.transform import MyProjectionTransformer
from .common.interpolation import BaseInterpolation  # Or a custom interpolation

def register_default_projections():
    # existing gnomonic, mercator, etc.
    
    # Register your new projection
    ProjectionRegistry.register("my_projection", {
        "config": MyProjectionConfig,
        "grid_generation": MyProjectionGridGeneration,
        "projection_strategy": MyProjectionStrategy,
        "interpolation": BaseInterpolation,   # or your own if you created a custom class
        "transformer": MyProjectionTransformer
    })
```
## 8. Using Your New Projection

After registration, you can retrieve an instance of your projection in two ways:
	1.	Get the BaseProjectionConfig only:

```python
from gnomonic.projection.registry import ProjectionRegistry
my_config = ProjectionRegistry.get_projection("my_projection", return_processor=False, R=6371.0, center_lat=45.0, ...)
```
Then manually create a ProjectionProcessor(my_config).

	2.	Get a fully equipped ProjectionProcessor in one call:
```python
processor = ProjectionRegistry.get_projection(
    "my_projection", return_processor=True,
    R=6371.0, center_lat=45.0, center_lon=0.0, ...
)
# Then use forward/backward
output_img = processor.forward(input_equirectangular_img)
back_to_eqrect = processor.backward(output_img)
```

## 9. Summary of the Pipeline
	1.	Forward Projection
	•	processor.forward(...) triggers:
	•	grid_generation.projection_grid(): your _projection_grid()
	•	projection_strategy.from_projection_to_spherical(x_grid, y_grid): your inverse math
	•	transformer.spherical_to_image_coords(lat, lon): to get pixel coords in original equirectangular
	•	interpolation.interpolate(...): actually remaps the pixels
	2.	Backward Projection
	•	processor.backward(...) triggers:
	•	grid_generation.spherical_grid(): your _spherical_grid()
	•	projection_strategy.from_spherical_to_projection(lat_grid, lon_grid): your forward math
	•	transformer.projection_to_image_coords(x, y): to get pixel coords in the new projection image
	•	interpolation.interpolate(...): remaps pixels from the rectilinear image back to equirect.

By following these instructions, you’ll have a fully integrated projection that the framework can use just like the existing gnomonic or mercator projections.

# Test

Write a test function such as
```python
import numpy as np
import cv2
from projection.registry import ProjectionRegistry
import matplotlib.pyplot as plt

def test_gnomonic_projection(image_path: str, output_dir: str):
    """
    Test the Gnomonic projection system by performing forward and backward projections.

    Args:
        image_path (str): Path to the input equirectangular image.
        output_dir (str): Directory to save the output images.
    """
    # Step 1: Load the equirectangular image
    equirect_img = cv2.imread(image_path)
    if equirect_img is None:
        raise RuntimeError(f"Failed to load the image at {image_path}.")
    H, W, _ = equirect_img.shape

    # Convert the image from BGR to RGB
    equirect_img = cv2.cvtColor(equirect_img, cv2.COLOR_BGR2RGB)

    # Step 2: Retrieve and instantiate a Gnomonic projection processor
    processor = ProjectionRegistry.get_projection(
        "gnomonic",
        return_processor=True,
        phi1_deg=0,
        lam0_deg=90,
        lat_points=H,
        lon_points=W,
        x_points=W // 4,
        y_points=H // 2,
        fov_deg=90
    )

    # Step 3: Perform forward projection to rectilinear
    rectilinear_img = processor.forward(equirect_img)
    rectilinear_path = f"{output_dir}/gnomonic_rectilinear.png"
    cv2.imwrite(rectilinear_path, cv2.cvtColor(rectilinear_img, cv2.COLOR_RGB2BGR))
    print(f"Gnomonic Rectilinear image saved to {rectilinear_path}")

    # Step 4: Perform backward projection to equirectangular
    equirectangular_img = processor.backward(
        rectilinear_img,
        return_mask=True,
    )
    equirectangular_path = f"{output_dir}/gnomonic_equirectangular.png"
    cv2.imwrite(equirectangular_path, cv2.cvtColor(equirectangular_img, cv2.COLOR_RGB2BGR))
    print(f"Gnomonic Equirectangular image saved to {equirectangular_path}")

    # Step 5: Mask pixels outside the projection area
    mask = np.mean(equirectangular_img, axis=-1) > 0

    # Step 6: Compute the Mean Absolute Error (MAE)
    mae_img = np.abs(equirect_img * mask[:, :, None] - equirectangular_img)
    mae = np.mean(mae_img[mask])
    print(f"Gnomonic Projection Mean Absolute Error: {mae}")

    # Step 7: Visualize the results
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 2, 1)
    plt.title("Gnomonic Rectilinear Image")
    plt.imshow(rectilinear_img)

    plt.subplot(1, 2, 2)
    plt.title("Gnomonic Equirectangular Image")
    plt.imshow(equirectangular_img)

    plt.show()

test_gnomonic_projection(image_path="data/image1.png", output_dir="results")
```