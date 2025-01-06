# projection/stereographic/__init__.py

"""
Stereographic Projection Module

This module provides specific implementations for Stereographic projections,
including configuration, projection strategies, and grid generation.

## Mathematical Foundation

The Stereographic projection projects points from a sphere onto a plane.
It is a conformal projection, preserving angles but not areas.

## Projection Processes

1. **Forward Projection:** 
   Maps points from geographic coordinates (lat/lon) to the stereographic projection plane.

2. **Inverse Projection:**
   Maps points from the stereographic projection plane back to geographic coordinates (lat/lon).

## Usage

See the example usage in the docstring below.
"""

import logging

from .config import StereographicConfig
from .strategy import StereographicProjectionStrategy
from .grid import StereographicGridGeneration
from .transform import StereographicTransformer
from ..logging_config import setup_logging

# Initialize logger for this module
logger = logging.getLogger('stereographic_projection.stereographic')

def initialize_stereographic_module():
    """
    Initialize the Stereographic Projection module.

    This initialization sets up any module-specific configurations or prerequisites.
    Currently, it primarily logs the initialization status.
    """
    logger.debug("Initializing Stereographic Projection Module.")
    # Any module-specific initialization can be done here
    logger.info("Stereographic Projection Module initialized successfully.")

# Call the initialization function upon import
initialize_stereographic_module()

__all__ = [
    "StereographicConfig",
    "StereographicProjectionStrategy",
    "StereographicGridGeneration",
    "StereographicTransformer"
]