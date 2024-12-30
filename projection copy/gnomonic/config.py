class GnomonicConfig:
    """
    Plain configuration class for Gnomonic projections, holding default parameters
    as a dictionary.
    """
    def __init__(self, **kwargs):
        """
        Initialize the configuration with default parameters.

        Args:
            **kwargs: Parameters to override default values.
        """
        # Default parameters
        self.params = {
            "R": 1.0,                # Radius of the sphere
            "phi1_deg": 0.0,         # Latitude of the projection center
            "lam0_deg": 0.0,         # Longitude of the projection center
            "fov_deg": 90.0,         # Field of view in degrees
            "x_points": 512,         # Number of grid points in x-direction
            "y_points": 512,         # Number of grid points in y-direction
            "lon_points": 1024,      # Number of longitude points for backward grid
            "lat_points": 512,       # Number of latitude points for backward grid
            "x_min": -1.0,           # Minimum x-coordinate in the grid
            "x_max": 1.0,            # Maximum x-coordinate in the grid
            "y_min": -1.0,           # Minimum y-coordinate in the grid
            "y_max": 1.0,            # Maximum y-coordinate in the grid
            "lon_min": -180.0,       # Minimum longitude in the grid
            "lon_max": 180.0,        # Maximum longitude in the grid
            "lat_min": -90.0,        # Minimum latitude in the grid
            "lat_max": 90.0,         # Maximum latitude in the grid
            "interpolation": None,   # Interpolation method (to be set downstream)
            "borderMode": None,      # Border mode for interpolation
            "borderValue": None,     # Border value for interpolation
        }
        self.params.update(kwargs)

    def update(self, **kwargs):
        """
        Update configuration parameters dynamically.

        Args:
            **kwargs: Parameters to update in the configuration.
        """
        self.params.update(kwargs)

    def __getitem__(self, key):
        """
        Enable dictionary-style access for configuration parameters.

        Args:
            key (str): Parameter name.

        Returns:
            The value of the parameter if it exists, or raises KeyError.
        """
        return self.params[key]

    def __setitem__(self, key, value):
        """
        Enable dictionary-style updates for configuration parameters.

        Args:
            key (str): Parameter name.
            value: New value for the parameter.
        """
        self.params[key] = value

    def __getattr__(self, item):
        """
        Access configuration parameters as attributes.

        Args:
            item (str): Attribute name.

        Returns:
            The value of the parameter if it exists, or raises AttributeError.
        """
        if item in self.params:
            return self.params[item]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __repr__(self):
        """
        String representation of the configuration.

        Returns:
            str: Human-readable string of configuration parameters.
        """
        return f"GnomonicConfig({self.params})"