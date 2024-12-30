### /Users/robinsongarcia/projects/gnomonic/projection/base/__init__.py ###

"""
Base module for gnomonic projection components.

This module includes base classes for projection configuration,
strategy, grid generation, interpolation, and coordinate transformations.
"""

from .config import BaseProjectionConfig
from .strategy import BaseProjectionStrategy
from .grid import BaseGridGeneration
from .interpolation import BaseInterpolation
from .transform import CoordinateTransformer

__all__ = [
    "BaseProjectionConfig",
    "BaseProjectionStrategy",
    "BaseGridGeneration",
    "BaseInterpolation",
    "CoordinateTransformer",
]