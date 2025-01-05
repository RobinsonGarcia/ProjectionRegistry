# projection/oblique_mercator/transform.py
import numpy as np
import logging
from ..base.transform import BaseCoordinateTransformer

logger = logging.getLogger("projection.oblique_mercator.transform")

class ObliqueMercatorTransformer(BaseCoordinateTransformer):
    """
    Maps (lat, lon) <-> (image coords) and (x, y) <-> (image coords),
    using the bounding box in the config for the equirectangular input 
    and the (fov_deg) approach for the forward-projection.
    """

    def spherical_to_image_coords(self, lat: np.ndarray, lon: np.ndarray, shape: tuple):
        """
        Map lat/lon [in degrees] onto equirectangular image coords (map_x, map_y).
        Equirect image shape: (height=H, width=W).
        """
        self._validate_inputs(lat, "lat")
        self._validate_inputs(lon, "lon")

        H, W = shape[:2]
        # Map longitude from [lon_min, lon_max] to [0, W-1]
        map_x = (lon - self.config.lon_min) / (self.config.lon_max - self.config.lon_min) * (W - 1)

        # Map latitude from [lat_max, lat_min] => [0, H-1] top to bottom
        map_y = (self.config.lat_max - lat) / (self.config.lat_max - self.config.lat_min) * (H - 1)

        return map_x, map_y

    def projection_to_image_coords(self, x: np.ndarray, y: np.ndarray, shape: tuple):
        """
        Map oblique (x, y) coords onto a 'rectilinear' image of size (x_points, y_points).
        Using fov_deg to define the max extent in x,y as ± R*tan(fov/2).
        """
        self._validate_inputs(x, "x")
        self._validate_inputs(y, "y")

        half_fov_rad = np.deg2rad(self.config.fov_deg / 2.0)
        max_val = np.tan(half_fov_rad) * self.config.R
        min_val = -max_val

        W, H = self.config.x_points, self.config.y_points

        map_x = (x - min_val) / (max_val - min_val) * (W - 1)
        map_y = (max_val - y) / (max_val - min_val) * (H - 1)

        return map_x, map_y