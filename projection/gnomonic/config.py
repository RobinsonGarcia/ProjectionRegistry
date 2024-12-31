from typing import Any, Optional
from pydantic import BaseModel, Field, validator
import cv2
import logging
from ..exceptions import ConfigurationError

# Initialize logger for this module
logger = logging.getLogger('gnomonic_projection.gnomonic.config')

class GnomonicConfigModel(BaseModel):
    R: float = Field(1.0, description="Radius of the sphere")
    phi1_deg: float = Field(0.0, description="Latitude of the projection center")
    lam0_deg: float = Field(0.0, description="Longitude of the projection center")
    fov_deg: float = Field(90.0, description="Field of view in degrees")
    x_points: int = Field(512, description="Number of grid points in x-direction")
    y_points: int = Field(512, description="Number of grid points in y-direction")
    lon_points: int = Field(1024, description="Number of longitude points for backward grid")
    lat_points: int = Field(512, description="Number of latitude points for backward grid")
    lon_min: float = Field(-180.0, description="Minimum longitude in the grid")
    lon_max: float = Field(180.0, description="Maximum longitude in the grid")
    lat_min: float = Field(-90.0, description="Minimum latitude in the grid")
    lat_max: float = Field(90.0, description="Maximum latitude in the grid")
    interpolation: Optional[int] = Field(default=cv2.INTER_LINEAR, description="Interpolation method for OpenCV remap")
    borderMode: Optional[int] = Field(default=cv2.BORDER_CONSTANT, description="Border mode for OpenCV remap")
    borderValue: Optional[Any] = Field(default=0, description="Border value for OpenCV remap")

    @validator('fov_deg')
    def validate_fov(cls, v):
        if not (0 < v < 180):
            raise ValueError("Field of view (fov_deg) must be between 0 and 180 degrees.")
        return v

    class Config:
        arbitrary_types_allowed = True

class GnomonicConfig:
    """
    Configuration class for Gnomonic projections using Pydantic for validation.
    """
    def __init__(self, **kwargs: Any) -> None:
        logger.debug("Initializing GnomonicConfig with parameters: %s", kwargs)
        try:
            self.config = GnomonicConfigModel(**kwargs)
            logger.info("GnomonicConfig initialized successfully.")
        except Exception as e:
            error_msg = f"Failed to initialize GnomonicConfig: {e}"
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from e

    def update(self, **kwargs: Any) -> None:
        logger.debug(f"Updating GnomonicConfig with parameters: {kwargs}")
        try:
            updated_config = self.config.copy(update=kwargs)
            self.config = updated_config
            logger.info("GnomonicConfig updated successfully.")
        except Exception as e:
            error_msg = f"Failed to update GnomonicConfig: {e}"
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from e

    def __getattr__(self, item: str) -> Any:
        logger.debug(f"Accessing GnomonicConfig attribute '{item}'.")
        try:
            return getattr(self.config, item)
        except AttributeError:
            error_msg = f"'GnomonicConfig' object has no attribute '{item}'"
            logger.error(error_msg)
            raise AttributeError(error_msg) from None

    def __repr__(self) -> str:
        return f"GnomonicConfig({self.config.dict()})"