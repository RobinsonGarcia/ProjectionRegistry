# projection/oblique_mercator/config.py

import logging
from typing import Any, Optional
from pydantic import BaseModel, Field, validator
import cv2
from ..exceptions import ConfigurationError

logger = logging.getLogger("projection.oblique_mercator.config")


class ObliqueMercatorConfigModel(BaseModel):
    R: float = Field(6371.0, description="Radius of the sphere (Earth) in kilometers.")
    center_lat: float = Field(40.0, description="Center latitude (degrees).")
    center_lon: float = Field(-100.0, description="Center longitude (degrees).")
    azimuth_deg: float = Field(30.0, description="Azimuth of the central line (degrees).")
    x_points: int = Field(1024, description="Number of points in x-direction.")
    y_points: int = Field(512, description="Number of points in y-direction.")
    lon_min: float = Field(-180.0, description="Minimum longitude for grid.")
    lon_max: float = Field(180.0, description="Maximum longitude for grid.")
    lat_min: float = Field(-85.0, description="Minimum latitude for grid.")
    lat_max: float = Field(85.0, description="Maximum latitude for grid.")
    interpolation: Optional[int] = Field(default=cv2.INTER_LINEAR, description="Interpolation method for OpenCV remap.")
    borderMode: Optional[int] = Field(default=cv2.BORDER_CONSTANT, description="Border mode for OpenCV remap.")
    borderValue: Optional[Any] = Field(default=0, description="Border value for OpenCV remap.")

    @validator("R")
    def validate_radius(cls, v):
        if v <= 0:
            raise ValueError("Radius must be > 0.")
        return v


class ObliqueMercatorConfig:
    def __init__(self, **kwargs: Any) -> None:
        logger.debug("Initializing ObliqueMercatorConfig with parameters: %s", kwargs)
        try:
            self.config = ObliqueMercatorConfigModel(**kwargs)
            logger.info("ObliqueMercatorConfig initialized successfully.")
        except Exception as e:
            logger.exception(f"Failed to initialize ObliqueMercatorConfig: {e}")
            raise ConfigurationError(str(e))

    def __getattr__(self, item: str) -> Any:
        return getattr(self.config, item)

    def __repr__(self) -> str:
        return f"ObliqueMercatorConfig({self.config.dict()})"