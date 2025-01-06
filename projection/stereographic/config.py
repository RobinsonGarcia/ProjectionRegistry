# projection/stereographic/config.py

import logging
from typing import Any, Optional
from pydantic import BaseModel, Field, validator
import cv2

from ..exceptions import ConfigurationError

logger = logging.getLogger("projection.stereographic.config")


class StereographicConfigModel(BaseModel):
    """
    Pydantic model for Stereographic projection configuration.

    Attributes include:
      - R (radius)
      - phi0_deg (center latitude)
      - lam0_deg (center longitude)
      - scaling factor (optional)
      - bounding box for lat/lon
      - resolution
      - interpolation settings
      - etc.
    """
    R: float = Field(6371.0, description="Radius of the Earth (or sphere) in kilometers.")
    phi0_deg: float = Field(0.0, description="Latitude center in degrees.")
    lam0_deg: float = Field(0.0, description="Longitude center in degrees.")

    x_points: int = Field(512, description="Number of points in x-direction.")
    y_points: int = Field(512, description="Number of points in y-direction.")
    lon_points: int = Field(1024, description="Number of longitude points for inverse grid mapping.")
    lat_points: int = Field(512, description="Number of latitude points for inverse grid mapping.")
    lon_min: float = Field(-180.0, description="Min longitude for grid.")
    lon_max: float = Field(180.0, description="Max longitude for grid.")
    lat_min: float = Field(-90.0, description="Min latitude for grid.")
    lat_max: float = Field(90.0, description="Max latitude for grid.")

    interpolation: Optional[int] = Field(default=cv2.INTER_LINEAR, description="OpenCV interpolation mode.")
    borderMode: Optional[int] = Field(default=cv2.BORDER_CONSTANT, description="OpenCV border mode.")
    borderValue: Optional[Any] = Field(default=0, description="OpenCV border value.")

    scaling_factor: Optional[float] = Field(default=1.0, description="Scaling factor for projection.")

    @validator("R")
    def validate_radius(cls, v):
        if v <= 0:
            raise ValueError("Sphere/Earth radius must be > 0.")
        return v

    @validator("scaling_factor")
    def validate_scaling_factor(cls, v):
        if v <= 0:
            raise ValueError("Scaling factor must be > 0.")
        return v

    class Config:
        arbitrary_types_allowed = True


class StereographicConfig:
    """
    Wrapper for StereographicConfigModel to be used by the rest of the system.
    Mirrors the design of GnomonicConfig, MercatorConfig, etc.
    """

    def __init__(self, **kwargs: Any) -> None:
        logger.debug("Initializing StereographicConfig with parameters: %s", kwargs)
        try:
            self.config = StereographicConfigModel(**kwargs)
            logger.info("StereographicConfig initialized successfully.")
        except Exception as e:
            error_msg = f"Failed to initialize StereographicConfig: {e}"
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from e

    def update(self, **kwargs: Any) -> None:
        """
        Dynamically update the projection parameters.
        """
        logger.debug(f"Updating StereographicConfig with parameters: {kwargs}")
        try:
            updated_config = self.config.copy(update=kwargs)
            self.config = updated_config
            logger.info("StereographicConfig updated successfully.")
        except Exception as e:
            error_msg = f"Failed to update StereographicConfig: {e}"
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from e

    def __getattr__(self, item: str) -> Any:
        """
        Access the pydantic config fields as attributes.
        """
        logger.debug(f"Accessing StereographicConfig attribute '{item}'.")
        try:
            return getattr(self.config, item)
        except AttributeError:
            error_msg = f"'StereographicConfig' object has no attribute '{item}'"
            logger.error(error_msg)
            raise AttributeError(error_msg)

    def __repr__(self) -> str:
        """
        String representation for debugging/logging.
        """
        return f"StereographicConfig({self.config.dict()})"