from typing import Any, Tuple
import numpy as np
import logging
from ..exceptions import TransformationError, ConfigurationError

# Initialize logger for this module
logger = logging.getLogger('gnomonic_projection.base.transform')

class BaseCoordinateTransformer:
    """
    Utility class for transforming coordinates between different systems.
    """

    def __init__(self, config) -> None:
        self.config = config

    @classmethod
    def spherical_to_image_coords(
        lat: np.ndarray, 
        lon: np.ndarray, 
        config: Any, 
        shape: Tuple[int, int, ...]
    ) -> Tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError("Subclasses must implement forward.")

    @staticmethod
    def projection_to_image_coords(
        x: np.ndarray, 
        y: np.ndarray, 
        config: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError("Subclasses must implement forward.")