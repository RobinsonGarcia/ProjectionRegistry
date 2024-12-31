### /Users/robinsongarcia/projects/gnomonic/projection/gnomonic/__init__.py ###

"""
Gnomonic Projection Module

This module provides specific implementations for Gnomonic projections,
including configuration, projection strategies, and grid generation.
"""

import logging

from .config import GnomonicConfig
from .strategy import GnomonicProjectionStrategy
from .grid import GnomonicGridGeneration
from ..logging_config import setup_logging

# Initialize logger for this module
logger = logging.getLogger('gnomonic_projection.gnomonic')

def initialize_gnomonic_module():
    """
    Initialize the Gnomonic Projection module.
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
]