### /Users/robinsongarcia/projects/gnomonic/projection/registry.py ###
from .base.config import BaseProjectionConfig

class _ProjectionRegistry:
    _registry = {}

    @classmethod
    def register(cls, name, components):
        """
        Register a projection with its required components.

        Args:
            name (str): Name of the projection (e.g., 'gnomonic').
            components (dict): A dictionary containing:
                - 'config': Configuration class (e.g., GnomonicConfig)
                - 'grid_generation': Grid generation class
                - 'projection_strategy': Projection strategy class
                - 'interpolation' (optional): Interpolation class
        """
        required_keys = {"config", "grid_generation", "projection_strategy"}
        if not required_keys.issubset(components):
            raise ValueError(f"Components must include {required_keys}. Missing keys: {required_keys - components.keys()}")
        cls._registry[name] = components

    @classmethod
    def get_projection(cls, name, **kwargs):
        """
        Retrieve a configured projection by name.

        Args:
            name (str): Name of the projection to retrieve.
            **kwargs: Configuration parameters to override defaults.

        Returns:
            BaseProjectionConfig: Configured projection object.
        """
        if name not in cls._registry:
            raise ValueError(f"Projection '{name}' not found in the registry.")

        # Retrieve components
        components = cls._registry[name]
        ConfigClass = components["config"]
        GridGenerationClass = components["grid_generation"]
        ProjectionStrategyClass = components["projection_strategy"]
        InterpolationClass = components.get("interpolation", None)

        # Instantiate the configuration object
        config_instance = ConfigClass(**kwargs)

        # Create a BaseProjectionConfig and attach the necessary methods
        base_config = BaseProjectionConfig(config_instance)
        base_config.create_projection = lambda: ProjectionStrategyClass(config_instance)
        base_config.create_grid_generation = lambda: GridGenerationClass(config_instance)
        if InterpolationClass:
            base_config.create_interpolation = lambda: InterpolationClass(config_instance)

        return base_config

    @classmethod
    def list_projections(cls):
        """List all registered projections."""
        return list(cls._registry.keys())
    

from .base.config import BaseProjectionConfig
from .processor import ProjectionProcessor

class ProjectionRegistry:
    _registry = {}

    @classmethod
    def register(cls, name, components):
        """
        Register a projection with its required components.

        Args:
            name (str): Name of the projection (e.g., 'gnomonic').
            components (dict): A dictionary containing:
                - 'config': Configuration class (e.g., GnomonicConfig)
                - 'grid_generation': Grid generation class
                - 'projection_strategy': Projection strategy class
                - 'interpolation' (optional): Interpolation class
        """
        required_keys = {"config", "grid_generation", "projection_strategy"}
        if not required_keys.issubset(components):
            raise ValueError(f"Components must include {required_keys}. Missing keys: {required_keys - components.keys()}")
        cls._registry[name] = components

    @classmethod
    def get_projection(cls, name, return_processor=False, **kwargs):
        """
        Retrieve a configured projection by name.

        Args:
            name (str): Name of the projection to retrieve.
            return_processor (bool): Whether to return the processor instead of the config.
            **kwargs: Configuration parameters to override defaults.

        Returns:
            BaseProjectionConfig or ProjectionProcessor: Depending on `return_processor`.
        """
        if name not in cls._registry:
            raise ValueError(f"Projection '{name}' not found in the registry.")

        # Retrieve components
        components = cls._registry[name]
        ConfigClass = components["config"]
        GridGenerationClass = components["grid_generation"]
        ProjectionStrategyClass = components["projection_strategy"]
        InterpolationClass = components.get("interpolation", None)

        # Instantiate the configuration object
        config_instance = ConfigClass(**kwargs)

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
    def list_projections(cls):
        """List all registered projections."""
        return list(cls._registry.keys())