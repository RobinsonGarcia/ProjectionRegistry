# projection/oblique_mercator/grid.py

import logging
import numpy as np
from typing import Tuple
from ..base.grid import BaseGridGeneration
from ..exceptions import GridGenerationError

logger = logging.getLogger("projection.oblique_mercator.grid")


class ObliqueMercatorGridGeneration(BaseGridGeneration):
    def projection_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        logger.debug("Generating Oblique Mercator forward grid.")
        try:
            x_vals = np.linspace(-self.config.R, self.config.R, self.config.x_points)
            y_vals = np.linspace(-self.config.R, self.config.R, self.config.y_points)
            return np.meshgrid(x_vals, y_vals)
        except Exception as e:
            logger.exception(f"Failed to generate forward grid: {e}")
            raise GridGenerationError(str(e))

    def spherical_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        logger.debug("Generating Oblique Mercator spherical grid.")
        try:
            lon_vals = np.linspace(self.config.lon_min, self.config.lon_max, self.config.x_points)
            lat_vals = np.linspace(self.config.lat_min, self.config.lat_max, self.config.y_points)
            return np.meshgrid(lon_vals, lat_vals)
        except Exception as e:
            logger.exception(f"Failed to generate spherical grid: {e}")
            raise GridGenerationError(str(e))