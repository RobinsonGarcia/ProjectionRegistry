from ..base.interpolation import BaseInterpolation

class BaseProjectionConfig:
    """
    Base class for projections, allowing dynamic initialization with configuration objects.
    """
    def __init__(self, config_object):
        """
        Initialize the projection configuration.

        Args:
            config_object: An object (e.g., GnomonicConfig) containing configuration parameters.
        """
        if not hasattr(config_object, "params"):
            raise ValueError("Configuration object must have a 'params' attribute.")
        self.config_object = config_object
        self.params = config_object.params
        self.extra_params = {}

    def create_projection(self):
        """
        Placeholder for creating a projection object.
        Subclasses or dynamic creation logic should override this method.
        """
        raise NotImplementedError("Subclasses or configuration must implement create_projection.")

    def create_grid_generation(self):
        """
        Placeholder for creating a grid generation object.
        Subclasses or dynamic creation logic should override this method.
        """
        raise NotImplementedError("Subclasses or configuration must implement create_grid_generation.")

    def create_interpolation(self):
        """
        Create an interpolation object using the configuration.
        """
        return BaseInterpolation(self)

    def update(self, **kwargs):
        """
        Update configuration parameters dynamically.

        Args:
            **kwargs: Parameters to update in the configuration.
        """
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value
            else:
                self.extra_params[key] = value

    def __getattr__(self, item):
        """
        Access configuration parameters as attributes.

        Args:
            item (str): Parameter name.

        Returns:
            The value of the parameter if it exists, or raises AttributeError.
        """
        if item in self.params:
            return self.params[item]
        if item in self.extra_params:
            return self.extra_params[item]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __repr__(self):
        """
        String representation of the configuration.

        Returns:
            str: Human-readable string of configuration parameters.
        """
        return f"BaseProjectionConfig(params={self.params}, extra_params={self.extra_params})"