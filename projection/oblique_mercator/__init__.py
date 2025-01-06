# projection/oblique_mercator/__init__.py

"""
Oblique Mercator Projection Package

Implements the Oblique Mercator projection by providing configuration,
grid generation, projection strategy, and coordinate transformation.
"""

from .config import ObliqueMercatorConfig
from .grid import ObliqueMercatorGridGeneration
from .strategy import ObliqueMercatorProjectionStrategy
from .transform import ObliqueMercatorTransformer

__all__ = [
    "ObliqueMercatorConfig",
    "ObliqueMercatorGridGeneration",
    "ObliqueMercatorProjectionStrategy",
    "ObliqueMercatorTransformer",
]