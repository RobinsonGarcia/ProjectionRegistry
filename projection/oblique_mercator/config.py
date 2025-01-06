# /Users/robinsongarcia/projects/gnomonic/projection/oblique_mercator/config.py
# projection/oblique_mercator/config.py
import logging
from typing import Any, Optional
from pydantic import BaseModel, Field, validator
import cv2

from ..exceptions import ConfigurationError

logger = logging.getLogger("projection.oblique_mercator.config")

class ObliqueMercatorConfigModel(BaseModel):
    """
    Configuration model (Pydantic) for the Oblique Mercator projection on a sphere.
    Follows Snyder's formulas to define an oblique axis.
    """
    R: float = Field(6371.0, description="Radius of the sphere (in kilometers).")
    k0: float = Field(1.0, description="Scale factor along the central line.")

    center_lat: float = Field(40.0, description="Center latitude for the oblique line (degrees).")
    center_lon: float = Field(-100.0, description="Center longitude for the oblique line (degrees).")
    azimuth_deg: float = Field(30.0, description="Azimuth east of north of the oblique central line.")

    lon_min: float = Field(-180.0, description="Minimum longitude.")
    lon_max: float = Field(180.0, description="Maximum longitude.")
    lat_min: float = Field(-85.0, description="Minimum latitude.")
    lat_max: float = Field(85.0, description="Maximum latitude.")

    x_points: int = Field(1024, description="Number of points along the x-axis.")
    y_points: int = Field(512, description="Number of points along the y-axis.")

    fov_deg: float = Field(90.0, description="Field of view (degrees) for forward projection grids.")

    interpolation: Optional[int] = Field(default=cv2.INTER_LINEAR, description="Interpolation method")
    borderMode: Optional[int] = Field(default=cv2.BORDER_CONSTANT, description="OpenCV border mode")
    borderValue: Optional[Any] = Field(default=0, description="OpenCV border value")

    @validator('fov_deg')
    def validate_fov(cls, v):
        if not (0 < v <= 180):
            raise ValueError("fov_deg must be in range (0, 180].")
        return v

class ObliqueMercatorConfig:
    """
    Wrapper for the Pydantic model to integrate with the BaseProjectionConfig in your system.
    """

    def __init__(self, **kwargs: Any):
        """
        Initialize ObliqueMercatorConfig with Pydantic validation.

        Args:
            **kwargs: Configuration parameters.

        Raises:
            ConfigurationError: If initialization fails due to invalid parameters.
        """
        logger.debug("Initializing ObliqueMercatorConfig with parameters: %s", kwargs)
        try:
            self.config = ObliqueMercatorConfigModel(**kwargs)
            logger.info("ObliqueMercatorConfig initialized successfully.")
        except Exception as e:
            error_msg = f"Failed to initialize ObliqueMercatorConfig: {e}"
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from e

    def update(self, **kwargs: Any) -> None:
        """
        Update ObliqueMercatorConfig parameters dynamically.

        Args:
            **kwargs (Any): Parameters to update.

        Raises:
            ConfigurationError: If an error occurs during update.
        """
        logger.debug(f"Updating ObliqueMercatorConfig with parameters: {kwargs}")
        try:
            updated = self.config.copy(update=kwargs)
            self.config = updated
            logger.info("ObliqueMercatorConfig updated successfully.")
        except Exception as e:
            error_msg = f"Failed to update ObliqueMercatorConfig: {e}"
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from e

    def __getattr__(self, item: str) -> Any:
        """
        Access configuration parameters as attributes.

        Args:
            item (str): The attribute name.

        Returns:
            Any: The attribute value.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        try:
            return getattr(self.config, item)
        except AttributeError:
            error_msg = f"'ObliqueMercatorConfig' object has no attribute '{item}'"
            logger.error(error_msg)
            raise AttributeError(error_msg)

    def __repr__(self) -> str:
        return f"ObliqueMercatorConfig({self.config.dict()})"