# projection/oblique_mercator/transform.py

import logging
import numpy as np
from typing import Tuple, Any
from ..base.transform import BaseCoordinateTransformer
from ..exceptions import TransformationError

logger = logging.getLogger("projection.oblique_mercator.transform")


class ObliqueMercatorTransformer(BaseCoordinateTransformer):
    def spherical_to_image_coords(self, lat: np.ndarray, lon: np.ndarray, shape: Tuple[int, int]) -> Tuple[np.ndarray, np.ndarray]:
        logger.debug("Converting spherical coordinates to image coordinates.")
        H, W = shape
        map_x = (lon - self.config.lon_min) / (self.config.lon_max - self.config.lon_min) * (W - 1)
        map_y = (self.config.lat_max - lat) / (self.config.lat_max - self.config.lat_min) * (H - 1)
        return map_x, map_y

    def projection_to_image_coords(self, x: np.ndarray, y: np.ndarray, config: Any) -> Tuple[np.ndarray, np.ndarray]:
        logger.debug("Converting projection coordinates to image coordinates.")
        W, H = config.x_points, config.y_points
        map_x = ((x + self.config.R) / (2 * self.config.R)) * (W - 1)
        map_y = ((self.config.R - y) / (2 * self.config.R)) * (H - 1)
        return map_x, map_y