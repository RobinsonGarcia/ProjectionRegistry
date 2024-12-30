### /Users/robinsongarcia/projects/gnomonic/projection/base/config.py ###

from typing import Any, Dict
from ..base.interpolation import BaseInterpolation

class BaseProjectionConfig:
    """
    Base class for projections, allowing dynamic initialization with configuration objects.
    """
    def __init__(self, config_object: Any) -> None:
        """
        Initialize the projection configuration.

        Args:
            config_object (Any): An object (e.g., GnomonicConfig) containing configuration parameters.

        Raises:
            ValueError: If the configuration object does not have a 'params' attribute.
        """
        if not hasattr(config_object, "params"):
            raise ValueError("Configuration object must have a 'params' attribute.")
        self.config_object: Any = config_object
        self.params: Dict[str, Any] = config_object.params
        self.extra_params: Dict[str, Any] = {}

    def create_projection(self) -> Any:
        """
        Placeholder for creating a projection object.
        Subclasses or dynamic creation logic should override this method.

        Raises:
            NotImplementedError: If the method is not overridden by subclasses.
        """
        raise NotImplementedError("Subclasses or configuration must implement create_projection.")

    def create_grid_generation(self) -> Any:
        """
        Placeholder for creating a grid generation object.
        Subclasses or dynamic creation logic should override this method.

        Raises:
            NotImplementedError: If the method is not overridden by subclasses.
        """
        raise NotImplementedError("Subclasses or configuration must implement create_grid_generation.")

    def create_interpolation(self) -> BaseInterpolation:
        """
        Create an interpolation object using the configuration.

        Returns:
            BaseInterpolation: The interpolation object.
        """
        return BaseInterpolation(self)

    def update(self, **kwargs: Any) -> None:
        """
        Update configuration parameters dynamically.

        Args:
            **kwargs (Any): Parameters to update in the configuration.
        """
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value
            else:
                self.extra_params[key] = value

    def __getattr__(self, item: str) -> Any:
        """
        Access configuration parameters as attributes.

        Args:
            item (str): Parameter name.

        Returns:
            Any: The value of the parameter if it exists.

        Raises:
            AttributeError: If the parameter does not exist.
        """
        if item in self.params:
            return self.params[item]
        if item in self.extra_params:
            return self.extra_params[item]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __repr__(self) -> str:
        """
        String representation of the configuration.

        Returns:
            str: Human-readable string of configuration parameters.
        """
        return f"BaseProjectionConfig(params={self.params}, extra_params={self.extra_params})"