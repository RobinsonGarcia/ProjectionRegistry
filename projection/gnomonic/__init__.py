"""
Gnomonic Projection Module

This module provides specific implementations for Gnomonic projections,
including configuration, projection strategies, and grid generation.

## Mathematical Foundation

The Gnomonic projection transforms points on the surface of a sphere (e.g., Earth)
onto a plane using a projection point located at the center of the sphere.
This projection is based on the principles of spherical trigonometry and can be
derived using the following key equations:

1. **Projection Equations:**
   
   For an oblique Gnomonic projection centered at latitude \(\phi_0\) and longitude \(\lambda_0\),
   the mapping from geographic coordinates \((\phi, \lambda)\) to planar coordinates \((x, y)\)
   is given by:

   $$
   x = \frac{a \,\sin \psi \,\cos \phi \,\sin(\lambda - \lambda_0)}{\sin \phi_0 \,\sin \phi + \cos \phi_0 \,\cos \phi \,\cos(\lambda - \lambda_0)}
   $$

   $$
   y = \frac{a \,\sin \psi \bigl[\cos \phi_0 \,\sin \phi - \sin \phi_0 \,\cos \phi \,\cos(\lambda - \lambda_0)\bigr]}{\sin \phi_0 \,\sin \phi + \cos \phi_0 \,\cos \phi \,\cos(\lambda - \lambda_0)}
   $$

   Where:
   - \(a\) is the radius of the Earth.
   - \(\psi\) is the auxiliary angle defined by the relationship:

     $$
     \cos \psi = \sin \phi_0 \,\sin \phi + \cos \phi_0 \,\cos \phi \,\cos(\lambda - \lambda_0)
     $$

2. **Special Cases:**
   
   - **Polar Gnomonic Projection (\(\phi_0 = 90^\circ\)):**

     $$
     x = -\,aS \,\cot \phi \,\sin(\lambda - \lambda_0)
     $$

     $$
     y = aS \,\cot \phi \,\cos(\lambda - \lambda_0)
     $$

     In this case, all meridians appear as straight lines radiating from the center,
     and parallels as concentric circles.

The Gnomonic projection is particularly useful for mapping great circles as straight lines,
which is advantageous in navigation and aeronautics.

## Projection Processes

1. **Forward Projection:**
   
   The forward projection maps points from an equirectangular (input) image to the Gnomonic projection plane.
   This process involves:
   
   - **Grid Generation:** Creating a meshgrid on the Gnomonic projection plane based on the field of view (`fov_deg`) and the Earth's radius (`R`).
   - **Coordinate Transformation:** Converting geographic coordinates (latitude and longitude) from the input image to planar coordinates (`x`, `y`) on the projection plane using the projection equations.
   - **Image Mapping:** Interpolating the input image based on the transformed coordinates to generate the projected Gnomonic image.

2. **Backward Projection:**
   
   The backward projection maps points from the Gnomonic projection plane back to an equirectangular (output) image.
   This reverse process involves:
   
   - **Grid Generation:** Creating a meshgrid covering the full range of longitude and latitude defined by `lon_min`, `lon_max`, `lat_min`, and `lat_max`.
   - **Coordinate Transformation:** Converting planar coordinates (`x`, `y`) from the projection plane back to geographic coordinates (latitude and longitude) using the inverse of the projection equations.
   - **Image Mapping:** Interpolating the Gnomonic image based on the transformed coordinates to reconstruct the equirectangular output image.

These processes ensure accurate mapping between different projection systems, maintaining the integrity of geospatial data during transformations.

## Usage

To perform Gnomonic projections, utilize the provided classes:

- **GnomonicConfig:** Manage and validate projection configurations.
- **GnomonicGridGeneration:** Generate forward and backward grids for projection.
- **GnomonicProjectionStrategy:** Execute forward and backward projection transformations.

### Example:

```python
from gnomonic.projection.gnomonic import GnomonicConfig, GnomonicProjectionStrategy, GnomonicGridGeneration
from gnomonic.projection.processor import ProjectionProcessor
import cv2

# Initialize configuration
config = GnomonicConfig(
    R=6371.0,          # Earth's radius in kilometers
    phi1_deg=45.0,     # Projection center latitude
    lam0_deg=0.0,      # Projection center longitude
    fov_deg=90.0,      # Field of view
    x_points=1024,     # Grid resolution x
    y_points=1024,     # Grid resolution y
    lon_min=-180.0,
    lon_max=180.0,
    lat_min=-90.0,
    lat_max=90.0
)

# Initialize grid generation and projection strategy
grid_gen = GnomonicGridGeneration(config)
strategy = GnomonicProjectionStrategy(config)

# Initialize processor
processor = ProjectionProcessor(config, grid_gen, strategy)

# Load an equirectangular image
equirect_img = cv2.imread('equirectangular_map.jpg')

# Perform forward projection
gnomonic_img = processor.forward(equirect_img)

# Save the projected image
cv2.imwrite('gnomonic_projected_map.jpg', gnomonic_img)

# Perform backward projection
back_projected_img = processor.backward(gnomonic_img)

# Save the back-projected image
cv2.imwrite('back_projected_map.jpg', back_projected_img)
"""

import logging

from .config import GnomonicConfig
from .strategy import GnomonicProjectionStrategy
from .grid import GnomonicGridGeneration
from .transform import GnomonicTransformer
from ..logging_config import setup_logging
#from ..base.processor import BaseProjectionProcessor
# Initialize logger for this module
logger = logging.getLogger('gnomonic_projection.gnomonic')

def initialize_gnomonic_module():
    """
    Initialize the Gnomonic Projection module.

    This initialization sets up any module-specific configurations or prerequisites.
    Currently, it primarily logs the initialization status.
    """
    logger.debug("Initializing Gnomonic Projection Module.")
    # Any module-specific initialization can be done here
    logger.info("Gnomonic Projection Module initialized successfully.")

# Call the initialization function upon import
initialize_gnomonic_module()



__all__ = [
    "GnomonicConfig",
    "GnomonicProjectionStrategy",
    "GnomonicGridGeneration",
    "GnomonicTransformer"
]