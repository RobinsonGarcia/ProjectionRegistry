from .registry import ProjectionRegistry
from .default_projections import register_default_projections

# Automatically register default projections
register_default_projections()

__all__ = ["ProjectionRegistry"]

