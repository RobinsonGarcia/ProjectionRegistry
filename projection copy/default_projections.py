### /Users/robinsongarcia/projects/gnomonic/projection/default_projections.py ###
from .registry import ProjectionRegistry
from .gnomonic.config import GnomonicConfig
from .gnomonic.grid import GnomonicGridGeneration
from .gnomonic.strategy import GnomonicProjectionStrategy
from .base.interpolation import BaseInterpolation

def register_default_projections():
    """
    Register default projections with their components.
    """
    # Register Gnomonic projection
    ProjectionRegistry.register("gnomonic", {
        "config": GnomonicConfig,
        "grid_generation": GnomonicGridGeneration,
        "projection_strategy": GnomonicProjectionStrategy,
        "interpolation": BaseInterpolation,
    })

    # Additional projections can be registered here