### /Users/robinsongarcia/projects/gnomonic/projection/base/grid.py ###

from typing import Any, Tuple
import numpy as np

class BaseGridGeneration:
    """
    Base class for grid generation in projections.
    """
    def create_grid(self, direction: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create a grid based on the specified direction.

        Args:
            direction (str): Direction of grid creation ('forward' or 'backward').

        Returns:
            Tuple[np.ndarray, np.ndarray]: Generated grid arrays.

        Raises:
            NotImplementedError: If the method is not overridden by subclasses.
            ValueError: If the direction is invalid.
        """
        if direction not in ('forward', 'backward'):
            raise ValueError("Direction must be 'forward' or 'backward'.")
        raise NotImplementedError("Subclasses must implement create_grid.")