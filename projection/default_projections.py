### /Users/robinsongarcia/projects/gnomonic/projection/default_projections.py ###

from .registry import ProjectionRegistry
from .gnomonic.config import GnomonicConfig
from .gnomonic.grid import GnomonicGridGeneration
from .gnomonic.strategy import GnomonicProjectionStrategy
from .base.interpolation import BaseInterpolation
from .exceptions import RegistrationError
import logging

# Initialize logger for this module
logger = logging.getLogger('gnomonic_projection.default_projections')

def register_default_projections():
    """
    Register default projections with their components.
    """
    logger.debug("Registering default projections.")
    try:
        # Register Gnomonic projection
        ProjectionRegistry.register("gnomonic", {
            "config": GnomonicConfig,
            "grid_generation": GnomonicGridGeneration,
            "projection_strategy": GnomonicProjectionStrategy,
            "interpolation": BaseInterpolation,
        })
        logger.info("Default projection 'gnomonic' registered successfully.")
    except RegistrationError as e:
        logger.exception("Failed to register default projections.")
        raise RegistrationError(f"Failed to register default projections: {e}") from e
    except Exception as e:
        logger.exception("An unexpected error occurred while registering default projections.")
        raise RegistrationError(f"An unexpected error occurred: {e}") from e

    # Additional projections can be registered here
    logger.debug("All default projections registered.")