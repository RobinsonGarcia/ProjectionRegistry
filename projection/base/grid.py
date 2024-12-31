### /Users/robinsongarcia/projects/gnomonic/projection/base/grid.py ###

from typing import Any, Tuple
import numpy as np
import logging
from ..exceptions import GridGenerationError, ProcessingError

# Initialize logger for this module
logger = logging.getLogger('gnomonic_projection.base.grid')

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
            GridGenerationError: If the direction is invalid or method is not overridden.
        """
        logger.debug(f"Creating grid with direction '{direction}'.")
        if direction not in ('forward', 'backward'):
            error_msg = "Direction must be 'forward' or 'backward'."
            logger.error(error_msg)
            raise GridGenerationError(error_msg)
        logger.debug(f"Direction '{direction}' is valid.")
        try:
            # Attempt to call the overridden method in subclasses
            return self._create_grid(direction)
        except NotImplementedError as e:
            error_msg = "Subclasses must implement create_grid."
            logger.error(error_msg)
            raise GridGenerationError(error_msg) from e
        except Exception as e:
            error_msg = f"An unexpected error occurred while creating grid: {e}"
            logger.exception(error_msg)
            raise GridGenerationError(error_msg) from e

    def _create_grid(self, direction: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Internal method to be overridden by subclasses for grid creation.

        Args:
            direction (str): Direction of grid creation.

        Raises:
            NotImplementedError: If not overridden by subclasses.
        """
        logger.debug("BaseGridGeneration._create_grid called - should be overridden.")
        raise NotImplementedError("Subclasses must implement _create_grid.")