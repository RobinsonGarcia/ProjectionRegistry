### /Users/robinsongarcia/projects/gnomonic/projection/__init__.py ###

"""
Gnomonic Projection Package

This package provides functionalities for gnomonic projections,
including registry management and default projection registration.
"""

from .registry import ProjectionRegistry
from .default_projections import register_default_projections

# Automatically register default projections
try:
    register_default_projections()
except Exception as e:
    raise RuntimeError("Failed to register default projections.") from e

__all__ = ["ProjectionRegistry"]