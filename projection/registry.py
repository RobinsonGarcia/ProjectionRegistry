### /Users/robinsongarcia/projects/gnomonic/projection/registry.py ###

from typing import Any, Dict, Optional, Type, Union
from .base.config import BaseProjectionConfig
from .processor import ProjectionProcessor

class ProjectionRegistry:
    """
    Registry for managing projection configurations and their components.
    """
    _registry: Dict[str, Dict[str, Type[Any]]] = {}

    @classmethod
    def register(cls, name: str, components: Dict[str, Type[Any]]) -> None:
        """
        Register a projection with its required components.

        Args:
            name (str): Name of the projection (e.g., 'gnomonic').
            components (Dict[str, Type[Any]]): A dictionary containing:
                - 'config': Configuration class (e.g., GnomonicConfig)
                - 'grid_generation': Grid generation class
                - 'projection_strategy': Projection strategy class
                - 'interpolation' (optional): Interpolation class

        Raises:
            ValueError: If required components are missing.
            TypeError: If components are not of expected types.
        """
        required_keys = {"config", "grid_generation", "projection_strategy"}
        missing_keys = required_keys - components.keys()
        if missing_keys:
            raise ValueError(f"Components must include {required_keys}. Missing keys: {missing_keys}")

        # Optional 'interpolation' component
        if "interpolation" in components:
            interpolation = components["interpolation"]
            if not isinstance(interpolation, type):
                raise TypeError("'interpolation' component must be a class type.")

        # Validate that required components are classes
        for key in required_keys:
            component = components[key]
            if not isinstance(component, type):
                raise TypeError(f"'{key}' component must be a class type.")

        cls._registry[name] = components

    @classmethod
    def get_projection(
        cls, 
        name: str, 
        return_processor: bool = False, 
        **kwargs: Any
    ) -> Union[BaseProjectionConfig, ProjectionProcessor]:
        """
        Retrieve a configured projection by name.

        Args:
            name (str): Name of the projection to retrieve.
            return_processor (bool): Whether to return the processor instead of the config.
            **kwargs (Any): Configuration parameters to override defaults.

        Returns:
            Union[BaseProjectionConfig, ProjectionProcessor]: Depending on `return_processor`.

        Raises:
            ValueError: If the projection name is not found in the registry.
            KeyError: If required components are missing from the registry.
            RuntimeError: If instantiation of configuration fails.
        """
        if name not in cls._registry:
            raise ValueError(f"Projection '{name}' not found in the registry.")

        # Retrieve components
        components = cls._registry[name]
        try:
            ConfigClass = components["config"]
            GridGenerationClass = components["grid_generation"]
            ProjectionStrategyClass = components["projection_strategy"]
            InterpolationClass = components.get("interpolation", None)
        except KeyError as e:
            raise KeyError(f"Missing component in the registry: {e}") from e

        # Instantiate the configuration object
        try:
            config_instance = ConfigClass(**kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate config class '{ConfigClass.__name__}': {e}") from e

        # Create a BaseProjectionConfig and attach the necessary methods
        base_config = BaseProjectionConfig(config_instance)
        base_config.create_projection = lambda: ProjectionStrategyClass(config_instance)
        base_config.create_grid_generation = lambda: GridGenerationClass(config_instance)
        if InterpolationClass:
            base_config.create_interpolation = lambda: InterpolationClass(config_instance)

        if return_processor:
            return ProjectionProcessor(base_config)

        return base_config

    @classmethod
    def list_projections(cls) -> list:
        """
        List all registered projections.

        Returns:
            list: A list of projection names.
        """
        return list(cls._registry.keys())